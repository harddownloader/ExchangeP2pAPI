import os
from dateutil import parser

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from common.util.const import GOOGLE_SPREADSHEETS_CREDENTIALS_FILE, GOOGLE_SPREADSHEETS_TOKEN_FILE


SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def insert_new_row(new_order, spreadsheet_id):
    credentials = None
    if os.path.exists(GOOGLE_SPREADSHEETS_TOKEN_FILE):
        credentials = Credentials.from_authorized_user_file(GOOGLE_SPREADSHEETS_TOKEN_FILE, SCOPES)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(GOOGLE_SPREADSHEETS_CREDENTIALS_FILE, scopes=SCOPES)
            credentials = flow.run_local_server(port=0)
        with open(GOOGLE_SPREADSHEETS_TOKEN_FILE, "w") as token:
            token.write(credentials.to_json())

    try:
        service = build("sheets", "v4", credentials=credentials)
        sheets = service.spreadsheets()

        list = [
            [
                new_order['date'],
                new_order['orderId'],
                new_order['card'],
                new_order['payoutAmount'],
            ],
        ]
        resource = {
            "majorDimension": "ROWS",
            "values": list
        }
        range = "Sheet1!A:A";
        sheets.values().append(
            spreadsheetId=spreadsheet_id,
            range=range,
            body=resource,
            valueInputOption="USER_ENTERED"
        ).execute()
    except HttpError as error:
        print(error)


if __name__ == "__main__":
    order_sample = {
        "date": parser.parse("2023-05-22T12:30:01+03:00", ignoretz=True),
        "orderId": "someOrderId",
        "card": "4444444444444444",
        "payoutAmount": "14.51",
    }
    SPREADSHEET_ID = "1g4WkcgKodgz5JNw2_Mk214mb_eWqxAi5TuBP9Kkbu_g"

    insert_new_row(order_sample, SPREADSHEET_ID)
