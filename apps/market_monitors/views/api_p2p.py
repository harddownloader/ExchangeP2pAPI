import hmac
import hashlib
import simplejson as json
import time
import logging
import gspread
import requests
from typing import List, Dict
from urllib3.util.retry import Retry
from urllib.parse import urlencode
import traceback
import pprint
from requests.adapters import HTTPAdapter
from sentry_sdk import capture_message

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import viewsets, status
from rest_framework.response import Response

from apps.market_monitors.const import BUY_TRADE_TYPE, SELL_TRADE_TYPE
from apps.market_monitors.models import Radar
from apps.markets.models import FiatCurrency, PayTypes, MarketAccount
from apps.orders.serializers import P2PMarketOrdersSerializer
from common.spreadsheets import (
    add_or_update_p2p_orders_list,
    check_or_gen_table_with_sheet_name
)
from common.const import (
    BASE_URL,
    GET_METHOD,
    POST_METHOD, DEFAULT_BINANCE_ACCOUNT_ID,
)

from common.exceptions import (
    CustomErrors,
    GETTING_MARKET_P2P_ORDERS_FROM_BINANCE,
    GOOGLE_SPREADSHEET_DOC_NOT_FOUND,
    ACCESS_TO_GOOGLE_SPREADSHEET,
    ACCESS_TO_GOOGLE_SPREADSHEET_UNREGISTERED_CASE
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def hashing(query_string, binance_secret_key: str):
    return hmac.new(
        binance_secret_key.encode("utf-8"),
        query_string.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()


def get_timestamp():
    offset = 15000
    return int(time.time() * 1000) - offset


def dispatch_request(http_method: str, binance_key: str):
    session = requests.Session()
    retry = Retry(connect=1, backoff_factor=1)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    session.headers.update({
        "Content-Type": "application/json;charset=utf-8",
        "X-MBX-APIKEY": binance_key
    })

    wrapper = {
        "GET": session.get,
        "DELETE": session.delete,
        "PUT": session.put,
        "POST": session.post,
    }

    try:
        return wrapper.get(http_method)
    except requests.exceptions as e:
        print(traceback.format_exc())
        return None


# used for sending request requires the signature
def send_signed_request(
        http_method: str,
        url_path: str,
        query_params={},
        body={},
        binance_creds={} # {key, secret}
):
    query_string = urlencode(query_params, True)
    if query_string:
        query_string = "{}&timestamp={}".format(query_string, get_timestamp())
    else:
        query_string = "timestamp={}".format(get_timestamp())

    url = (
        BASE_URL + url_path + "?" + query_string + "&signature=" + hashing(query_string, binance_secret_key=binance_creds['secret'])
    )
    print("{} {}".format(http_method, url))
    params = {"url": url, "params": {}}
    if http_method is not GET_METHOD:
        params["data"] = json.dumps(body)

    response = dispatch_request(http_method, binance_key=binance_creds['key'])(**params)

    try:
        return response.json()
    except json.decoder.JSONDecodeError as e:
        print(traceback.format_exc())
        return None


# used for sending public data request
def send_public_request(
        url_path: str,
        payload={},
        binance_creds={} # {key, secret}
):
    query_string = urlencode(payload, True)
    url = BASE_URL + url_path
    if query_string:
        url = url + "?" + query_string
    print("{}".format(url))
    response = dispatch_request(GET_METHOD, binance_key=binance_creds['key'])(url=url)

    return response.json()


""" ======  end of functions ====== """

class P2PMarketOrdersViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def list(self, request):
        logger.info('get_market_p2p_orders', exc_info=1)

        serializer = P2PMarketOrdersSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        market_monitor_id = validated_data.get('market_monitor_id')

        try:
            market_monitor_inst = Radar.objects.get(pk=int(market_monitor_id))
            market_monitor = json.loads(json.dumps(market_monitor_inst, default=vars, use_decimal=True))
        except Radar.DoesNotExist:
            return Response("market monitor by this ID not found", status=status.HTTP_404_NOT_FOUND)

        try:
            binance_account_inst = MarketAccount.objects.get(pk=int(DEFAULT_BINANCE_ACCOUNT_ID))
            binance_account = json.loads(json.dumps(binance_account_inst, default=vars))
            binance_creds: Dict[str, str] = {
                'key': binance_account['api_key'],
                'secret': binance_account['secret_key'],
            }
        except Radar.DoesNotExist:
            return Response("default market account not found", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if "doc_id" in market_monitor and market_monitor["doc_id"]:
            doc_id = market_monitor["doc_id"]
        else:
            return Response("'doc_id' not exists in market_monitor", status=status.HTTP_404_NOT_FOUND)

        if "sheet_name" in market_monitor and market_monitor["sheet_name"]:
            sheet_name = market_monitor["sheet_name"]
        else:
            return Response("'sheet_name' not exists in market_monitor", status=status.HTTP_404_NOT_FOUND)

        if "first_row" in market_monitor and isinstance(market_monitor["first_row"], int) and market_monitor["first_row"] >= 0:
            first_row = market_monitor["first_row"]
        else:
            return Response("'first_row' not exists in market_monitor", status=status.HTTP_404_NOT_FOUND)

        try:
            fiat = FiatCurrency.objects.get(pk=market_monitor["fiat_id"]).name
        except FiatCurrency.DoesNotExist:
            return Response("'fiat' of market_monitor not found", status=status.HTTP_404_NOT_FOUND)

        try:
            pay_type = PayTypes.objects.get(pk=market_monitor["pay_type_id"]).name
        except PayTypes.DoesNotExist:
            return Response("'pay_type' of market_monitor not found", status=status.HTTP_404_NOT_FOUND)

        if "trade_type" in market_monitor and market_monitor["trade_type"] in [BUY_TRADE_TYPE, SELL_TRADE_TYPE]:
            trade_type = market_monitor["trade_type"]
        else:
            return Response("correct 'trade_type' of market_monitor was not found", status=status.HTTP_404_NOT_FOUND)


        client_type_options = ('web', 'ios', 'android')
        sort_options = ('asc', 'desc')
        params = {
            'recvWindow': 60000, # use it for all requests
            'clientType': client_type_options[0]
        }
        body = {
            "additionalKycVerifyFilter": 0,
            "asset": "USDT",
            "countries": [],
            "fiat": fiat,
            "filterType": "all",
            # "order"
            "page": 1,
            "payTypes": [pay_type],
            "publisherType": None,
            "rows": 10,
            "sort": sort_options[0],
            "tradeType": trade_type,
            "transAmount": market_monitor["transAmount"]
        }

        time = send_public_request("/api/v3/time", binance_creds=binance_creds).get('serverTime', None)
        ads = send_signed_request(
            POST_METHOD,
            "/sapi/v1/c2c/ads/search",
            params,
            body,
            binance_creds=binance_creds
        )

        if ads and 'data' in ads and len(ads['data']) and ads['code'] == '000000':
            try:
                check_or_gen_table_with_sheet_name(
                    spreadsheet_id=doc_id,
                    sheet_name=sheet_name,
                )
                add_or_update_p2p_orders_list(
                    orders=ads['data'],
                    spreadsheet_id=doc_id,
                    sheet_name=sheet_name,
                    first_row=int(first_row),
                )
            except gspread.exceptions.APIError as e:
                if e.code == 403:
                    capture_message("api_p2p.py->P2PMarketOrdersViewSet->list. " +
                                    "Server does not have enough permission to work with current google spreadsheet doc." +
                                    f"doc_id={doc_id} sheet_name={sheet_name}. " +
                                    "Please share this doc with your email that you received from google cloud console(creds) " +
                                    "and give it access as Editor")
                    return Response(
                        CustomErrors(ACCESS_TO_GOOGLE_SPREADSHEET).generate_response(),
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )

                capture_message("api_p2p.py->P2PMarketOrdersViewSet->list. " +
                                "gspread.exceptions.APIError: unknown case." +
                                f"doc_id={doc_id} sheet_name={sheet_name}. " +
                                f"code: {e.code}")
                return Response(
                    CustomErrors(ACCESS_TO_GOOGLE_SPREADSHEET_UNREGISTERED_CASE).generate_response(),
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            except PermissionError as e:
                capture_message("api_p2p.py->P2PMarketOrdersViewSet->list. " +
                                "Server does not have permission to google spreadsheet doc." +
                                f"doc_id={doc_id} sheet_name={sheet_name}. " +
                                "Please share this doc with your email that you received from google cloud console(creds)" +
                                "and give it access as Editor")
                return Response(
                    CustomErrors(ACCESS_TO_GOOGLE_SPREADSHEET).generate_response(),
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            except gspread.exceptions.WorksheetNotFound:
                capture_message("api_p2p.py->P2PMarketOrdersViewSet->list. " +
                                "Server can not found google spreadsheet doc." +
                                f"doc_id={doc_id} sheet_name={sheet_name}. " +
                                "Please check the google spreadsheet doc ID and try again.")
                return Response(
                    CustomErrors(GOOGLE_SPREADSHEET_DOC_NOT_FOUND).generate_response(),
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            except Exception as e:
                capture_message("api_p2p.py->P2PMarketOrdersViewSet->list. " +
                                f"doc_id={doc_id} sheet_name={sheet_name}. " +
                                "Something went wrong with updating p2p market orders into the google spreadsheet")

                return Response(
                        CustomErrors(GETTING_MARKET_P2P_ORDERS_FROM_BINANCE).generate_response(),
                        status=status.HTTP_502_BAD_GATEWAY
                    )
        else:
            capture_message("api_p2p.py->P2PMarketOrdersViewSet->list. " +
                            "The server did not receive p2p orders data from binance. " +
                            f"ads={json.loads(json.dumps(ads))}")
            return Response(
                CustomErrors(GETTING_MARKET_P2P_ORDERS_FROM_BINANCE).generate_response(),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response({
            "time": time,
            "ads": ads
        }, status=status.HTTP_201_CREATED)
