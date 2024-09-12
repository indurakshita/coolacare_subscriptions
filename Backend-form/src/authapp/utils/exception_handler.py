from rest_framework.views import exception_handler


def handle_exception(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        response_data = {
            "type":"Error" or response.type  ,
            "message": response.data.get("detail", "An error occurred."),
            "code": response.status_code,
        }
        response.data = response_data
    return response