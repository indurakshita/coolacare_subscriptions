from django.utils.functional import SimpleLazyObject
from common.authentication import get_user_data
from django.contrib.auth import login


class UserDataMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.user = None

    def __call__(self, request):
        self.user = get_user_data(request)
        request.user_data = self.user
        response = self.get_response(request)
        return response
