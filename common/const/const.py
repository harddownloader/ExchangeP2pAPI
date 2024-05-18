import os
from django.conf import settings
from dotenv import load_dotenv

load_dotenv()

# google spreadsheets
GOOGLE_SPREADSHEETS_CREDENTIALS_INFO =\
    os.getenv("GOOGLE_CREDENTIALS_INFO")
MAIN_SPREADSHEET_DOC_ID=os.getenv("MAIN_SPREADSHEET_DOC_ID")

# binance
BASE_URL = "https://api.binance.com"  # production base url
DEFAULT_BINANCE_ACCOUNT_ID = os.getenv("DEFAULT_BINANCE_ACCOUNT_ID")

# http methods
GET_METHOD = "GET"
POST_METHOD = "POST"
PATCH_METHOD = "PATCH"
PUT_METHOD = "PUT"
DELETE_METHOD = "DELETE"

# pem keys
PUBLIC_KEY = bytes(os.getenv("PUBLIC_KEY"), encoding='utf8').decode('unicode_escape')
PRIVATE_KEY = bytes(os.getenv("PRIVATE_KEY"), encoding='utf8').decode('unicode_escape')