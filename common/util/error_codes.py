INSERT_ORDER_INTO_SPREADSHEET = "INSERT_ORDER_INTO_SPREADSHEET"

class CustomErrors:
    def __init__(self, message, code):
        self.message = message
        self.code = code
    def __str__(self):
        return "{code}: {message}".format(code=self.code, message=self.message)

    def get_code(self):
        return self.code

    def get_message(self):
        return self.message

ERROR_CODES = {
    f'{INSERT_ORDER_INTO_SPREADSHEET}': CustomErrors("Something went wrong", 1)
}
