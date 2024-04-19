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


def get_admin_base_path() -> str:
    """Gets the API base path

    Returns:
        str: Base path
    """
    return f"{environment.auth_api_base_url}{auth_consts.ADMIN_PATH}{auth_consts.REALMS_PATH}"


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


def get_auth_tokens_for_credentials(
    realm: str, payload: models.GetTokensForCredentialsPayload
) -> requests.Response:
    """Gets the authorization tokens for the credentials and realm in context

    Args:
        realm (str): The realm in context
        payload (models.GetTokensForCredentialsPayload): The required payload to get tokens

    Returns:
        requests.Response: The response from the auth API.
    """
    url = f"{get_base_path()}{realm}{auth_consts.AUTH_TOKENS_PATH}"
    data = urlencode(
        {
            "grant_type": constants.CLIENT_CREDENTIALS_GRANT_TYPE,
            "client_id": payload.clientId,
            "client_secret": payload.clientSecret,
            "scope": payload.scope,
        }
    )
    return requests.post(
        url, headers=common_headers, data=data, timeout=constants.TIMEOUT
    )


def register_new_user(
    realm: str, authorization: str, payload: models.RegisterUserPayload
) -> requests.Response:
    """Registers a new user

    Args:
        realm (str): The realm in context
        authorization (str): Authorization access token
        payload (models.RegisterUserPayload): The required payload to register an user

    Returns:
        requests.Response: The response from the auth API.
    """
    url = f"{get_admin_base_path()}{realm}{auth_consts.AUTH_USERS_PATH}"
    data = {
        "username": payload.username,
        "enabled": True,
        "email": payload.email,
        "firstName": payload.firstName,
        "lastName": payload.lastName,
        "credentials": [{"type": "password", "value": payload.password}],
    }
    return requests.post(
        url,
        headers={
            "Content-Type": constants.JSON_CONTENT_TYPE,
            "Authorization": authorization,
        },
        json=data,
        timeout=constants.TIMEOUT,
    )


def login_user(realm: str, payload: models.LoginUserPayload) -> requests.Response:
    """Logins an user

    Args:
        realm (str): The realm in context
        payload (models.LoginUserPayload): The required payload to login an user

    Returns:
        requests.Response: The response from the auth API.
    """
    url = f"{get_base_path()}{realm}{auth_consts.AUTH_TOKENS_PATH}"
    data = urlencode(
        {
            "grant_type": constants.PASSWORD_GRANT_TYPE,
            "client_id": payload.clientId,
            "client_secret": payload.clientSecret,
            "scope": payload.scope,
            "username": payload.username,
            "password": payload.password,
        }
    )
    return requests.post(
        url, headers=common_headers, data=data, timeout=constants.TIMEOUT
    )


def logout(realm: str, authorization: str, user_id: str) -> requests.Response:
    """Logs out an existing user

    Args:
        realm (str): The realm in context
        authorization (str): Authorization access token
        user_id (str): The id of the user to log out

    Returns:
        requests.Response: The response from the auth API.
    """
    base_path = f"{get_admin_base_path()}{realm}{auth_consts.AUTH_USERS_PATH}"
    url = f"{base_path}/{user_id}{auth_consts.AUTH_LOGOUT_PATH}"
    return requests.post(
        url,
        headers={
            "Content-Type": constants.JSON_CONTENT_TYPE,
            "Authorization": authorization,
        },
        timeout=constants.TIMEOUT,
    )


def send_reset_password_email(
    realm: str, authorization: str, user_id: str
) -> requests.Response:
    """Sends an email to reset the user password

    Args:
        realm (str): The realm in context
        authorization (str): Authorization access token
        user_id (str): The id of the user to send the reset password email

    Returns:
        requests.Response: The response from the auth API.
    """
    base_path = f"{get_admin_base_path()}{realm}{auth_consts.AUTH_USERS_PATH}"
    url = f"{base_path}/{user_id}{auth_consts.AUTH_RESET_PASSWORD_EMAIL}"
    return requests.put(
        url,
        headers={
            "Content-Type": constants.JSON_CONTENT_TYPE,
            "Authorization": authorization,
        },
        timeout=constants.TIMEOUT,
    )

def get_users_by_email(
    realm: str, authorization: str, email: str
) -> requests.Response:
    """Gets users by email

    Args:
        realm (str): The realm in context
        authorization (str): Authorization access token
        email (str): The email of the user

    Returns:
        requests.Response: The response from the auth API.
    """
    url = f"{get_admin_base_path()}{realm}{auth_consts.AUTH_USERS_PATH}?email={email}"
    return requests.get(
        url,
        headers={
            "Content-Type": constants.JSON_CONTENT_TYPE,
            "Authorization": authorization,
        },
        timeout=constants.TIMEOUT,
    )
