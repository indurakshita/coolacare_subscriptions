from rest_framework import pagination
from django.conf import settings
from common.configs import ConfigParser


config = ConfigParser("settings.pagination")
page = config.load(settings.ENVIRON)


class Pagination(pagination.PageNumberPagination):
    page_size = page.get("page_size")
    page_query_param = page.get("page_query_param")
    page_size_query_param = page.get("page_size_query_param")
    max_page_size = page.get("max_page_size")
