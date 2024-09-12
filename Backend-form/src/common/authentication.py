from typing import List, Optional
import requests
from rest_framework.exceptions import AuthenticationFailed
from py_eureka_client import eureka_client
from config.spring import ConfigClient
from common.utils import input_json
from django.conf import settings
from pydantic import BaseModel, Field


class UserAuthority(BaseModel):
    authority: str


class User(BaseModel):
    password: Optional[str]
    username: str
    authorities: List[UserAuthority]
    account_non_expired: bool = Field(alias="accountNonExpired")
    account_non_locked: bool = Field(alias="accountNonLocked")
    credentials_non_expired: bool = Field(alias="credentialsNonExpired")
    enabled: bool
    user_id: int = Field(alias="userId")
    organization_id: int = Field(alias="organizationId")
    language_code: str = Field(alias="languageCode")
    full_name: str = Field(alias="fullName")


def authorize(request):
    """
    This function is used to authorize the user based on the authorization token passed in the request headers.
    It uses the Eureka client to fetch the user details from the user management service and returns the user details along with the authorities.

    Args:
        request (HttpRequest): The incoming request object containing the authorization token in the headers.

    Returns:
        tuple: A tuple containing the user details and the authorities.

    Raises:
        AuthenticationFailed: If the authorization fails, this exception is raised.
    """
    try:
        client = ConfigClient()
        client.get_config()
        prefer_ip = client.config["eureka"]["instance"]["preferIpAddress"]

        def authorize_client(url):
            return requests.get(
                url,
                headers={"Authorization": request.headers.get("Authorization")},
                timeout=1,
            )

        response = eureka_client.walk_nodes(
            "USER-MANAGEMENT",
            "/auth/v1/user",
            prefer_ip=prefer_ip,
            walker=authorize_client,
        )

        if response.status_code == 401:
            raise AuthenticationFailed(
                code=401,
                detail="Cannot perform authorization at this time. Please try again later.",
            )
        user = response.json()
        user = User(**user)
        return user
    except:
        return None


def mock_authorization():
    """
    This function is used to mock the authorization process.
    It returns a mock user with the specified authorities.

    Returns:
        tuple: A tuple containing the mock user and the authorities.
    """
    user = {
        "password": None,
        "username": "admin",
        "authorities": [
            {"authority": "BLOCK_USER"},
            {"authority": "CREATE_ORGANIZATION"},
            {"authority": "CREATE_ROLE"},
            {"authority": "DELETE_ORGANIZATION"},
            {"authority": "DELETE_ROLE"},
            {"authority": "DELETE_USER"},
            {"authority": "INVITE_USER"},
            {"authority": "READ_ORGANIZATION"},
            {"authority": "READ_ORGANIZATIONS"},
            {"authority": "READ_ROLE"},
            {"authority": "READ_USER"},
            {"authority": "READ_USERS"},
            {"authority": "ROLE_PROVIDER_ADMIN"},
            {"authority": "SUPER_ADMIN"},
            {"authority": "UPDATE_ORGANIZATION"},
            {"authority": "UPDATE_ROLE"},
            {"authority": "UPDATE_USER"},
            {"authority": "UPDATE_USER_ROLE"},
        ],
        "accountNonExpired": True,
        "accountNonLocked": True,
        "credentialsNonExpired": True,
        "enabled": True,
        "userId": 1,
        "organizationId": 1,
        "languageCode": "en-US",
        "fullName": "Albin:albin",
    }
    user = User(**user)
    return user


def get_user_data(request=None):
    """
    This function is used to get the user data based on the incoming request.
    If the request is present and the DEBUG mode is enabled, it will mock the authorization process.
    Otherwise, it will use the authorize function to fetch the user details from the user management service.

    Args:
        request (HttpRequest): The incoming request object containing the authorization token in the headers.

    Returns:
        OneCareUser: The user instance.

    Raises:
        AuthenticationFailed: If the authorization fails.
    """
    try:
        if settings.DEBUG:
            user = mock_authorization()
        elif request:
            user = authorize(request)
    except Exception as e:
        user = str(e)

    return user
