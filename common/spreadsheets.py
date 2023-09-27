import os
import json
from dateutil import parser

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from common.util.const import (
    GOOGLE_SPREADSHEETS_CREDENTIALS_FILE,
    GOOGLE_SPREADSHEETS_TOKEN_FILE,
    GOOGLE_SPREADSHEETS_CREDENTIALS_INFO,
)

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


# create credentials.json on first run app (from env data)
def init_spreadsheets_credentials_json_file(cred_data: str):
    with open(GOOGLE_SPREADSHEETS_CREDENTIALS_FILE, "w") as token:
        token.write(
            json.dumps(
                json.loads(cred_data)
            )
        )
    return


def get_credentials():
    credentials = None
    if os.path.exists(GOOGLE_SPREADSHEETS_TOKEN_FILE):
        credentials = Credentials.from_authorized_user_file(
            GOOGLE_SPREADSHEETS_TOKEN_FILE,
            SCOPES
        )

    if (
            not credentials and
            not os.path.exists(GOOGLE_SPREADSHEETS_CREDENTIALS_FILE) and
            "GOOGLE_CREDENTIALS_INFO" in os.environ and
            os.getenv('GOOGLE_CREDENTIALS_INFO') is not None
    ):
        init_spreadsheets_credentials_json_file(GOOGLE_SPREADSHEETS_CREDENTIALS_INFO)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                GOOGLE_SPREADSHEETS_CREDENTIALS_FILE,
                scopes=SCOPES
            )
            credentials = flow.run_local_server(port=0)
        with open(GOOGLE_SPREADSHEETS_TOKEN_FILE, "w") as token:
            token.write(credentials.to_json())

    return credentials


# add new row to google spreadsheets
def insert_new_row(new_order, spreadsheet_id):
    credentials = get_credentials()

    try:
        service = build("sheets", "v4", credentials=credentials)
        sheets = service.spreadsheets()

        row_data = [
            [
                new_order['date'],
                new_order['orderId'],
                new_order['card'],
                new_order['payoutAmount'],
            ],
        ]
        resource = {
            "majorDimension": "ROWS",
            "values": row_data
        }
        table_range = "Sheet1!A:A"
        sheets.values().append(
            spreadsheetId=spreadsheet_id,
            range=table_range,
            body=resource,
            valueInputOption="USER_ENTERED"
        ).execute()
    except HttpError as error:
        print(error)


if __name__ == "__main__":
    order_sample = {
        # "date": parser.parse("2023-05-22T12:30:01+03:00", ignoretz=True),
        "date": parser.parse("2023-05-22T12:30:01", ignoretz=True),
        "orderId": "someOrderId",
        "card": "4444444444444444",
        "payoutAmount": "14.51",
        "callbackUrl": "http://localhost:7000/api/v1/callback/1/",
        "callbackMethod": "PATCH",
        "callbackHeaders": json.dumps({
            "custom-header-key-1": "custom-header-value-1",
            "custom-header-key-2": "custom-header-value-2",
            "custom-header-key-3": "custom-header-value-3"
        }, separators=(',', ':')),
        "callbackBody": json.dumps({
            "custom-body-key-1": "custom-body-value-1",
            "custom-body-key-2": "custom-body-value-2"
        }, separators=(',', ':')),
    }
    SPREADSHEET_ID = "1g4WkcgKodgz5JNw2_Mk214mb_eWqxAi5TuBP9Kkbu_g"

    insert_new_row(order_sample, SPREADSHEET_ID)
