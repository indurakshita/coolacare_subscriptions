from rest_framework.response import Response as Default


class Response:
    @staticmethod
    def error(message, status_code=400):
        return Default({"error": message}, status=status_code)

    @staticmethod
    def success(data, status_code=200):
        return Default(data, status=status_code)
