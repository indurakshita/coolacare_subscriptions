from common.exceptions import BaseCustomExceptions
from rest_framework import status


class NoResponse(BaseCustomExceptions):
    detail = "No Response Returned"
    status_code = status.HTTP_404_NOT_FOUND


class ConfigPathException(BaseCustomExceptions):
    detail = "Config Path Not Found"
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class DuplicateObjectCreationException(BaseCustomExceptions):
    detail = "Duplicate Object Created"
    status_code = status.HTTP_400_BAD_REQUEST


class ValidationError(BaseCustomExceptions):
    detail = "Validation error occurred"
    status_code = status.HTTP_400_BAD_REQUEST


class ObjectDoesNotExist(BaseCustomExceptions):
    detail = "Object does not exist"
    status_code = status.HTTP_404_NOT_FOUND

