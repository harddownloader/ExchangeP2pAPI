import os
from dateutil import parser

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from common.util.const import GOOGLE_SPREADSHEETS_CREDENTIALS_FILE, GOOGLE_SPREADSHEETS_TOKEN_FILE


SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

SPREADSHEET_ID = "1g4WkcgKodgz5JNw2_Mk214mb_eWqxAi5TuBP9Kkbu_g"


def main(newOrder):
    credentials = None
    if os.path.exists("../token.json"):
        credentials = Credentials.from_authorized_user_file("../token.json", SCOPES)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(GOOGLE_SPREADSHEETS_CREDENTIALS_FILE, scopes=SCOPES)
            credentials = flow.run_local_server(port=0)
        with open("../token.json", "w") as token:
            token.write(credentials.to_json())

    try:
        service = build("sheets", "v4", credentials=credentials)
        sheets = service.spreadsheets()

        # result = sheets\
        #     .values()\
        #     .get(spreadsheetId=SPREADSHEET_ID, range="Sheet1!A1:C6")\
        #     .execute()
        # values = result.get("values", [])
        #
        # for row in values:
        #     print(values)
        list = [
            [
                newOrder['orderId'],
                newOrder['date'],
                newOrder['status'],
                newOrder['payoutAmount'],
                newOrder['card']
            ],
            # ["valuea2"], # row2
            # ["valuea3"], # row3
        ]
        resource = {
            "majorDimension": "ROWS",
            "values": list
        }
        range = "Sheet1!A:A";
        sheets.values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=range,
            body=resource,
            valueInputOption="USER_ENTERED"
        ).execute()
    except HttpError as error:
        print(error)


if __name__ == "__main__":
    orderSample = {
        "date": parser.parse("2023-05-22T12:30:01+03:00", ignoretz=True),
        "orderId": "someOrderId",
        "card": "4444444444444444",
        "payoutAmount": "14.51",
    }
    main(orderSample)
