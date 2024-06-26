# binance
GETTING_MARKET_P2P_ORDERS_FROM_BINANCE = "GETTING_MARKET_P2P_ORDERS_FROM_BINANCE"

# google spreadsheets
INSERT_ORDER_INTO_SPREADSHEET = "INSERT_ORDER_INTO_SPREADSHEET"
ACCESS_TO_GOOGLE_SPREADSHEET = "ACCESS_TO_GOOGLE_SPREADSHEET"
ACCESS_TO_GOOGLE_SPREADSHEET_UNREGISTERED_CASE = "ACCESS_TO_GOOGLE_SPREADSHEET_UNREGISTERED_CASE"
GOOGLE_SPREADSHEET_DOC_NOT_FOUND = "GOOGLE_SPREADSHEET_DOC_NOT_FOUND"

# partner
PARTNER_DOC_NOT_FOUND = "PARTNER_DOC_NOT_FOUND"

"""
Dict of all custom errors.
Structure:
'key_of_error': tuple( output_message, custom_error_code )
"""
ERROR_CODES = {
    f'{GETTING_MARKET_P2P_ORDERS_FROM_BINANCE}': ("Something went wrong", 1),
    f'{INSERT_ORDER_INTO_SPREADSHEET}': ("Something went wrong", 2),
    f'{ACCESS_TO_GOOGLE_SPREADSHEET}': ("Something went wrong", 3),
    f'{ACCESS_TO_GOOGLE_SPREADSHEET_UNREGISTERED_CASE}': ("Something went wrong", 4),
    f'{GOOGLE_SPREADSHEET_DOC_NOT_FOUND}': ("Something went wrong", 5),
    f'{PARTNER_DOC_NOT_FOUND}': ("Partner google doc not found", 6)
}
