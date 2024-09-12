from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from authapp.models.validationmodel import ApiLabel

def validate_response(label):
    message = get_object_or_404(ApiLabel, label=label)
    response = {
        "type": message.type,
        "message": message.message,
        "code": message.status_code,
    }
    return Response(response, status=message.status_code)

def validate_error(label):
    message = get_object_or_404(ApiLabel, label=label)
    response = {
        "type": message.type,
        "message": message.message,
        "code": message.status_code,
    }
    return response
