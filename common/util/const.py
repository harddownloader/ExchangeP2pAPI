import os
from django.conf import settings
from dotenv import load_dotenv

load_dotenv()

GOOGLE_SPREADSHEETS_CREDENTIALS_FILE =\
    os.path.join(settings.BASE_DIR, 'credentials.json')
GOOGLE_SPREADSHEETS_TOKEN_FILE =\
    os.path.join(settings.BASE_DIR, 'token.json')
GOOGLE_SPREADSHEETS_CREDENTIALS_INFO =\
    os.getenv("GOOGLE_CREDENTIALS_INFO")
