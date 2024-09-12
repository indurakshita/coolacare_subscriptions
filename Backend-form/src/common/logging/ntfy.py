from typing import Literal, Union
from common.configs import ConfigParser
from common.http import make_request


def ntfy_notification(message, conf: Union[Literal["general", "test"], bool]="test"):
    config = ConfigParser("settings.ntfy")
    ntfy_configs = config.load(conf)
    url = f"{ntfy_configs['server']}/{ntfy_configs['topic']}" 
    return make_request(url=url, method="post", json={"message":message})


