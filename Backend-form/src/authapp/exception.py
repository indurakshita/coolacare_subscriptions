from rest_framework.exceptions import APIException

class CustomException(APIException):
    def __init__(self,type=None, detail=None, status_code=None):
        self.type = type
        self.detail = detail
        self.status_code = status_code
         

    def __str__(self):
        return self.detail