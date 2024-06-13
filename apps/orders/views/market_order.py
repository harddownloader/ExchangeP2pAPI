import os
import hmac
import hashlib
import simplejson as json
import time
import logging
import gspread
import requests
from typing import List, Dict
import cv2
import pyotp

from django.conf import settings
from rest_framework.decorators import api_view
from urllib3.util.retry import Retry
from urllib.parse import urlencode
import traceback
import pprint
from requests.adapters import HTTPAdapter
from sentry_sdk import capture_message

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import viewsets, status
from rest_framework.response import Response

from apps.market_monitors.const import BUY_TRADE_TYPE, SELL_TRADE_TYPE
from apps.market_monitors.models import Radar
from apps.market_monitors.views import send_signed_request
from apps.markets.binance import params
from apps.markets.models import FiatCurrency, PayTypes, MarketAccount
from apps.orders.serializers import P2PMarketOrdersSerializer
from common.spreadsheets import (
    add_or_update_p2p_orders_list,
    check_or_gen_table_with_sheet_name
)
from common.const import (
    BASE_URL,
    GET_METHOD,
    POST_METHOD,
    DEFAULT_BINANCE_ACCOUNT_ID,
)

from common.exceptions import (
    CustomErrors,
    GETTING_MARKET_P2P_ORDERS_FROM_BINANCE,
    GOOGLE_SPREADSHEET_DOC_NOT_FOUND,
    ACCESS_TO_GOOGLE_SPREADSHEET,
    ACCESS_TO_GOOGLE_SPREADSHEET_UNREGISTERED_CASE
)

from apps.orders.const import AUTO_REPLY_MSG

class CreateMarketOrderView(generics.CreateAPIView):
    def get(self, request, *args, **kwargs):
        try:
            binance_account_inst = MarketAccount.objects.get(pk=int(DEFAULT_BINANCE_ACCOUNT_ID))
            binance_account = json.loads(json.dumps(binance_account_inst, default=vars))
            binance_creds: Dict[str, str] = {
                'key': binance_account['api_key'],
                'secret': binance_account['secret_key'],
            }
        except Radar.DoesNotExist:
            return Response("default market account not found", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response("get", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        try:
            binance_account_inst = MarketAccount.objects.get(pk=int(DEFAULT_BINANCE_ACCOUNT_ID))
            binance_account = json.loads(json.dumps(binance_account_inst, default=vars))
            binance_creds: Dict[str, str] = {
                'key': binance_account['api_key'],
                'secret': binance_account['secret_key'],
            }
        except Radar.DoesNotExist:
            return Response("default market account not found", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # qr_code_img = os.path.join(settings.MEDIA_ROOT, 'binance1_qr.jpg')
        # # Load the QR code image
        # qr_cv2_img = cv2.imread(qr_code_img)
        # # Initialize the QR code detector
        # detector = cv2.QRCodeDetector()
        #
        # # Detect and decode the QR code
        # val = detector.detectAndDecode(qr_cv2_img)
        # print(val[0])

        # Initialize the TOTP object
        totp = pyotp.TOTP(binance_account['google_auth_totp_code'])

        # Generate the Google Authenticator code
        google_code = totp.now()

        order_body = {
            "asset": "USDT",
            "authType": "GOOGLE",
            "autoReplyMsg": AUTO_REPLY_MSG, #"string",
            # "buyerBtcPositionLimit": 0,
            "buyerKycLimit": 0,
            "buyerRegDaysLimit": 90, # 0,
            "classify": "profession", # "string",
            "code": google_code, # "string",
            # "emailVerifyCode": "string",
            "fiatUnit": "UAH",  # "string",
            "googleVerifyCode": google_code, # "string",
            "initAmount": 100,
            "maxSingleTransAmount": 4000,
            "minSingleTransAmount": 3500,
            # "mobileVerifyCode": "string",
            # "onlineDelayTime": 0,
            "onlineNow": False,  # true,
            "payTimeLimit": 15, # 0
            "price": 43.00,
            # "priceFloatingRatio": 0,
            "priceType": 1, # "priceType": 0,
            # "rateFloatingRatio": 0,
            # "remarks": "string",
            # "saveAsTemplate": 0,
            # "takerAdditionalKycRequired": 0,
            # "templateName": "string",
            # "tradeMethods": [
            #     {
            #         "identifier": "string",
            #         "payId": 0,
            #         "payType": "string"
            #     }
            # ],
            "tradeMethods": [
                {
                    "identifier": "PrivatBank",
                    # "payId": 0,
                    # "payType": "string" # Deprecated. Please use identifier.
                }
            ],
            "tradeType": "SELL",
            # "userAllTradeCountMax": 0,
            # "userAllTradeCountMin": 0,
            # "userBuyTradeCountMax": 0,
            # "userBuyTradeCountMin": 0,
            # "userSellTradeCountMax": 0,
            # "userSellTradeCountMin": 0,
            # "userTradeCompleteCountMin": 0,
            # "userTradeCompleteRateFilterTime": 0,
            # "userTradeCompleteRateMin": 0,
            # "userTradeCountFilterTime": 0,
            # "userTradeType": 0,
            # "userTradeVolumeAsset": "string",
            # "userTradeVolumeFilterTime": 0,
            # "userTradeVolumeMax": 0,
            # "userTradeVolumeMin": 0,
            # "yubikeyVerifyCode": "string"
        }

        pprint.pprint(order_body, indent=4)

        new_order = send_signed_request(
            POST_METHOD,
            "/sapi/v1/c2c/ads/post",
            params,
            order_body,
            binance_creds=binance_creds
        )
        return Response(new_order, status=status.HTTP_201_CREATED)
