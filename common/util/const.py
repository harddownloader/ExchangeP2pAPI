import os
from django.conf import settings
from dotenv import load_dotenv

load_dotenv()

# google spreadsheets
GOOGLE_SPREADSHEETS_CREDENTIALS_INFO =\
    os.getenv("GOOGLE_CREDENTIALS_INFO")
MAIN_SPREADSHEET_DOC_ID=os.getenv("MAIN_SPREADSHEET_DOC_ID")
MAIN_SPREADSHEET_DOC_TAB=os.getenv("MAIN_SPREADSHEET_DOC_TAB")
MAIN_SPREADSHEET_DOC_START_ROW=os.getenv("MAIN_SPREADSHEET_DOC_START_ROW")

# binance
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_SECRET_KEY = os.getenv("BINANCE_SECRET_KEY")
BASE_URL = "https://api.binance.com"  # production base url

# http methods
GET_METHOD = "GET"
POST_METHOD = "POST"
PATCH_METHOD = "PATCH"
PUT_METHOD = "PUT"
DELETE_METHOD = "DELETE"