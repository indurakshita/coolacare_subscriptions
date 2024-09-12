from django.http import JsonResponse
from common.exceptions import NoResponse, ConfigPathException
from rest_framework.views import APIView


def user_data(request):
    return JsonResponse({"user": request.user_data.model_dump()})


class TestException(APIView):
    def get(self, request):
        raise NoResponse
