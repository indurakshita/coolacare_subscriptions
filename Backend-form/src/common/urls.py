from django.urls import path
from common import views


urlpatterns = [
    path("exceptions/", views.TestException.as_view(), name="exceptions"),
    path("user/", views.user_data, name="user"),
]
