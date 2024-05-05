import hmac
import hashlib
import requests
from requests.adapters import HTTPAdapter
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from urllib3.util.retry import Retry
import json
import time
import logging
from urllib.parse import urlencode
import traceback

from sentry_sdk import capture_message

from apps.orders.serializers import P2PMarketOrdersSerializer
from common.spreadsheets import add_or_update_p2p_orders_list
from common.util.const import (
    BINANCE_API_KEY,
    BINANCE_SECRET_KEY,
    MAIN_SPREADSHEET_DOC_ID,
    MAIN_SPREADSHEET_DOC_TAB,
    BASE_URL,
    GET_METHOD,
    POST_METHOD, MAIN_SPREADSHEET_DOC_START_ROW
)

from rest_framework import viewsets, status
from rest_framework.response import Response

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def hashing(query_string):
    return hmac.new(
        BINANCE_SECRET_KEY.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256
    ).hexdigest()


def get_timestamp():
    offset = 15000
    return int(time.time() * 1000) - offset


def dispatch_request(http_method):
    session = requests.Session()
    retry = Retry(connect=1, backoff_factor=1)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    session.headers.update({
        "Content-Type": "application/json;charset=utf-8",
        "X-MBX-APIKEY": BINANCE_API_KEY
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
def send_signed_request(http_method, url_path, query_params={}, body={}):
    query_string = urlencode(query_params, True)
    if query_string:
        query_string = "{}&timestamp={}".format(query_string, get_timestamp())
    else:
        query_string = "timestamp={}".format(get_timestamp())

    url = (
        BASE_URL + url_path + "?" + query_string + "&signature=" + hashing(query_string)
    )
    print("{} {}".format(http_method, url))
    params = {"url": url, "params": {}}
    if http_method is not GET_METHOD:
        params["data"] = json.dumps(body)

    response = dispatch_request(http_method)(**params)

    try:
        return response.json()
    except json.decoder.JSONDecodeError as e:
        print(traceback.format_exc())
        return None


# used for sending public data request
def send_public_request(url_path, payload={}):
    query_string = urlencode(payload, True)
    url = BASE_URL + url_path
    if query_string:
        url = url + "?" + query_string
    print("{}".format(url))
    response = dispatch_request(GET_METHOD)(url=url)
    return response.json()


""" ======  end of functions ====== """

class P2PMarketOrdersViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def list(self, request):
        logger.info('get_market_p2p_orders', exc_info=1)

        serializer = P2PMarketOrdersSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        trade_type = validated_data.get('tradeType')
        pay_type = validated_data.get('payType')


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
            "fiat": "UAH",
            "filterType": "all",
            # "order"
            "page": 1,
            "payTypes": [pay_type],
            "publisherType": None,
            "rows": 10,
            "sort": sort_options[0],
            "tradeType": trade_type
            # "transAmount":
        }

        time = send_public_request("/api/v3/time").get('serverTime', None)
        ads = send_signed_request(POST_METHOD, "/sapi/v1/c2c/ads/search", params, body)

        if ads and len(ads['data']) and ads['code'] == '000000':
            add_or_update_p2p_orders_list(
                orders=ads['data'],
                spreadsheet_id=MAIN_SPREADSHEET_DOC_ID,
                sheet_name=MAIN_SPREADSHEET_DOC_TAB,
                first_row=int(MAIN_SPREADSHEET_DOC_START_ROW)
            )
        else:
            capture_message("Something went wrong with putting p2p orders into the google spreadsheet")
            print(f'Something went wrong with putting p2p orders into the google spreadsheet. ads={ads}')
        return Response({
            "time": time,
            "ads": ads
        }, status=status.HTTP_201_CREATED)
