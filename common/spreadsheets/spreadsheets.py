import json
import gspread
import traceback

from gspread.utils import ValueInputOption

from common.spreadsheets.p2p_order_mapper import p2p_order_mapper
from common.util.const import (
    GOOGLE_SPREADSHEETS_CREDENTIALS_INFO,
)

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# add new row to google spreadsheets
def add_order_into_table(new_order, spreadsheet_id, sheet_name):
    try:
        credentials =  json.loads(GOOGLE_SPREADSHEETS_CREDENTIALS_INFO)
        gc = gspread.service_account_from_dict(credentials)
        sh = gc.open_by_key(spreadsheet_id)
        worksheet = sh.worksheet(sheet_name)

        table_content = worksheet.get_all_values()
        num_rows = len(table_content)
        num_last_row = ++num_rows
        row_data = [
                "",
                "",
                new_order['date'],
                new_order['orderId'],
                new_order['card'],
                "",
                new_order['payoutAmount'],
            ]
        worksheet.append_row(row_data, table_range=f'A{num_last_row}:G{num_last_row}')
    except Exception as e:
        print(traceback.format_exc())

        return None


def add_or_update_p2p_orders_list(orders: dict, spreadsheet_id: str, sheet_name: str, first_row: int):
    try:
        credentials =  json.loads(GOOGLE_SPREADSHEETS_CREDENTIALS_INFO)
        gc = gspread.service_account_from_dict(credentials)
        sh = gc.open_by_key(spreadsheet_id)
        worksheet = sh.worksheet(sheet_name)

        rows_data = []
        for order in orders:
            rows_data.append(
                list(
                    p2p_order_mapper(order['adv']) # mapped data
                        .values() # get only values of dict
                )
            )

        new_rows_length = len(rows_data)
        worksheet.insert_rows(
            rows_data,
            row=first_row,
            value_input_option=ValueInputOption.raw,
        )

        # clearing prev notes
        start_clearing_row = first_row + new_rows_length
        end_clearing_row = first_row + (new_rows_length * 2)
        worksheet.delete_rows(start_clearing_row, end_clearing_row)
    except Exception as e:
        print(traceback.format_exc())

        return None