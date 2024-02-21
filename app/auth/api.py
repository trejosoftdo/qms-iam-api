"""Auth API
"""

from urllib.parse import urlencode
import requests
from .. import environment
from .. import constants
from . import models
from . import constants as auth_consts


common_headers = {"Content-Type": constants.FORM_URL_ENCODED}


def get_base_path() -> str:
    """Gets the API base path

    Returns:
        str: Base path
    """
    return f"{environment.auth_api_base_url}{auth_consts.REALMS_PATH}"


def auth_device(
    realm: str, payload: models.AuthorizeDevicePayload
) -> requests.Response:
    """Authorizes a device to a realm in context via the auth API

    Args:
      realm (str): The realm in context
      payload (str): The required payload

    Returns:
        requests.Response: The response from the auth API.
    """
    url = f"{get_base_path()}{realm}{auth_consts.AUTH_DEVICE_PATH}"
    payload = urlencode(
        {
            "client_id": payload.clientId,
            "client_secret": payload.clientSecret,
            "scope": payload.scope,
        }
    )
    return requests.post(
        url, headers=common_headers, data=payload, timeout=constants.TIMEOUT
    )


def get_auth_tokens(realm: str, payload: models.GetTokensPayload) -> requests.Response:
    """Gets the authorization tokens for the given device code and realm in context

    Args:
        realm (str): The realm in context
        payload (models.GetTokensPayload): The required payload to authorize

    Returns:
        requests.Response: The response from the auth API.
    """
    url = f"{get_base_path()}{realm}{auth_consts.AUTH_TOKENS_PATH}"
    payload = urlencode(
        {
            "device_code": payload.deviceCode,
            "grant_type": constants.DEVICE_TOKEN_GRANT_TYPE,
            "client_id": payload.clientId,
            "client_secret": payload.clientSecret,
        }
    )
    return requests.post(
        url, headers=common_headers, data=payload, timeout=constants.TIMEOUT
    )


def token_instrospect(
    realm: str, access_token: str, payload: models.ValidateAccessTokenPayload
) -> requests.Response:
    """Gets information such as scope and active from the given token

    Args:
        realm (str): The realm in context
        access_token (str): The token to instrospect
        payload (models.ValidateAccessTokenPayload): The required payload to intronspect the token

    Returns:
        requests.Response: The response from the auth API.
    """
    url = f"{get_base_path()}{realm}{auth_consts.INSTROSPECT_PATH}"
    payload = urlencode(
        {
            "token": access_token,
            "client_id": payload.clientId,
            "client_secret": payload.clientSecret,
        }
    )
    return requests.post(
        url, headers=common_headers, data=payload, timeout=constants.TIMEOUT
    )


def get_new_access_token(
    realm: str, payload: models.GetNewAccessTokenPayload
) -> requests.Response:
    """Gets a new access token

    Args:
        realm (str): The realm in context
        payload (models.GetNewAccessTokenPayload): The required payload to get the new access token

    Returns:
        requests.Response: The response from the auth API.
    """
    url = f"{get_base_path()}{realm}{auth_consts.AUTH_TOKENS_PATH}"
    payload = urlencode(
        {
            "refresh_token": payload.refreshToken,
            "grant_type": constants.REFRESH_TOKEN_GRANT_TYPE,
            "client_id": payload.clientId,
            "client_secret": payload.clientSecret,
        }
    )
    return requests.post(
        url, headers=common_headers, data=payload, timeout=constants.TIMEOUT
    )
