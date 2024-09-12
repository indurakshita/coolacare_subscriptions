import requests


def make_request(url: str, method: str = "get", *args, **kwargs):
    response = requests.request(method=method, url=url, *args, **kwargs)
    return response
