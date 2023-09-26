import os
from definitions import ROOT_DIR
from dotenv import load_dotenv

load_dotenv()

print("ROOT_DIR" + ROOT_DIR)
GOOGLE_SPREADSHEETS_CREDENTIALS_FILE = os.path.join(ROOT_DIR, '/credentials2.json')
GOOGLE_SPREADSHEETS_TOKEN_FILE = os.path.join(ROOT_DIR, '/token.json')
GOOGLE_SPREADSHEETS_CREDENTIALS_INFO = os.getenv("GOOGLE_CREDENTIALS_INFO")
