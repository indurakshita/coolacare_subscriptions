from typing import Union, Literal
from common.configs import ConfigParser
from common.logging import logger
from common.http import make_request
from rest_framework.exceptions import APIException


class BaseCustomExceptions(APIException):
    __module__ = APIException.__module__
    detail = "Exception raised"
    status_code = 500

    def __init__(
        self,
        detail: str = None,
        log: bool = False,
        priority: str = "debug",
        ntfy: Union[Literal["general", "exceptions", "test"], bool] = False,
    ):
        self.detail = detail or self.detail
        self.priority = priority
        self.ntfy = ntfy
        self.log = log
        self.mapper()

    def _log(self, message: Union[str, None] = None):
        message = message or self.message
        log = getattr(logger, self.priority)
        log(message)

    def mapper(self):
        if self.log:
            self._log()

        if self.ntfy:
            self.ntfy_notification()
        return self

    def ntfy_notification(self):
        config = ConfigParser("settings.ntfy")
        ntfy_configs = config.load(self.ntfy)

        url = f"{ntfy_configs['server']}/{ntfy_configs['topic']}"
        client = make_request(url=url, method="post", data=self.message)

        if not client.connection:
            self._log("Failed to send notification")
        else:
            self._log(f"Notification sent to server='{url}'")
        return self

    def __str__(self):
        return self.message
