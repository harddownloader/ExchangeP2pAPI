from .const import ERROR_CODES

class CustomErrors:
    def __init__(self, error_action):
        self.message = ERROR_CODES[error_action][0]
        self.code = ERROR_CODES[error_action][1]

    def __str__(self):
        return "{code}: {message}".format(code=self.code, message=self.message)

    def get_code(self):
        return self.code

    def get_message(self):
        return self.message

    def generate_response(self):
        return {
            "error": self.message,
            "code": self.code
        }