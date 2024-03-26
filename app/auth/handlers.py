"""Auth API handlers
"""

from . import models
from . import api
from .helpers import handle_error_response
from .. import constants
from .. import exceptions


def authorize_device(
    realm: str, payload: models.AuthorizeDevicePayload
) -> models.AuthorizeDeviceResponse:
    """Authorizes a device to a realm in context via the auth API

    Args:
      realm (str): the realm in context
      payload (models.AuthorizeDevicePayload): the required payload

    Returns:
        models.AuthorizeDeviceResponse: Authorization information such as deviceCode,
        and userCode.
    """
    response = api.auth_device(realm, payload)

    handle_error_response(response)

    data = response.json()

    return models.AuthorizeDeviceResponse(
        data=models.AuthorizeDeviceResponseData(
            deviceCode=data.get("device_code"),
            userCode=data.get("user_code"),
            expiresIn=data.get("expires_in"),
            interval=data.get("interval"),
            verificationURI=data.get("verification_uri_complete"),
        )
    )


def get_auth_tokens(
    realm: str, payload: models.GetTokensPayload
) -> models.GetTokensResponse:
    """Gets the authorization tokens for the given device code and realm in context

    Args:
        realm (str): The realm in context
        payload (models.GetTokensPayload): The required payload

    Returns:
        models.GetTokensResponse: The authorization tokens information
    """
    response = api.get_auth_tokens(realm, payload)

    handle_error_response(response)

    data = response.json()

    return models.GetTokensResponse(
        data=models.GetTokensResponseData(
            accessToken=data.get("access_token"),
            refreshToken=data.get("refresh_token"),
            expiresIn=data.get("expires_in"),
            refreshExpiresIn=data.get("refresh_expires_in"),
        )
    )


def get_new_access_token(
    realm: str, payload: models.GetNewAccessTokenPayload
) -> models.GetNewAccessTokenResponse:
    """Gets a new authorization token for the given refresh token and realm in context

    Args:
        realm (str): The realm in context
        payload (models.GetNewAccessTokenPayload): The required payload to refresh token

    Returns:
        models.GetNewAccessTokenResponse: The new access token data
    """
    response = api.get_new_access_token(realm, payload)

    handle_error_response(response)

    data = response.json()

    return models.GetNewAccessTokenResponse(
        data=models.GetNewAccessTokenResponseData(
            accessToken=data.get("access_token"),
            expiresIn=data.get("expires_in"),
        )
    )


def validate_access_token(
    realm: str, authorization: str, payload: models.ValidateAccessTokenPayload
) -> models.ValidateAccessTokenResponse:
    """Validates a token checking if it has not expired and has the required scope

    Args:
        realm (str): The realm in context
        authorization (str): The authorization access token
        payload (models.ValidateAccessTokenPayload): The required payload to validate the token

    Raises:
      HTTPException: Internal server error when something unexpected happens.
      HTTPException: Authorization error when token is invalidd.
      HTTPException: Forbidden error when the lacking the expected scope.

    Returns:
        models.ValidateAccessTokenResponse: The new access token data
    """
    is_valid = False
    is_authorized = False
    access_token = authorization.replace(
        constants.BEARER_PORTION, constants.EMPTY_VALUE
    )

    try:
        response = api.token_instrospect(
            realm,
            access_token,
            payload,
        )
        data = response.json()
        is_valid = data.get(constants.ACTIVE_PROPERTY) is True
        scopes = data.get(constants.SCOPE_PROPERTY, constants.EMPTY_VALUE).split(
            constants.SCOPES_SEPARATOR
        )
        is_authorized = payload.expectedScope in scopes
    except Exception as exc:
        raise exceptions.INTERNAL_SERVER_ERROR from exc

    return models.ValidateAccessTokenResponse(
        data=models.ValidateAccessTokenResponseData(
            isValid=is_valid,
            isAuthorized=is_authorized,
            expectedScope=payload.expectedScope,
        )
    )


def get_user_basic_data(
    realm: str, authorization: str, payload: models.UserBasicDataPayload
) -> models.UserBasicDataResponse:
    """Gets the user basic information

    Args:
        realm (str): The realm in context
        authorization (str): The authorization access token
        payload (models.UserBasicDataPayload): The required payload to get user data

    Returns:
        models.UserBasicDataResponse: The user data
    """
    access_token = authorization.replace(
        constants.BEARER_PORTION, constants.EMPTY_VALUE
    )
    instrospect_payload = models.ValidateAccessTokenPayload(
        clientId=payload.clientId,
        clientSecret=payload.clientSecret,
        expectedScope="email",
    )
    response = api.token_instrospect(
        realm,
        access_token,
        instrospect_payload,
    )

    handle_error_response(response)

    data = response.json()
    return models.UserBasicDataResponse(
        data=models.UserBasicData(
            username=data.get("preferred_username", constants.EMPTY_VALUE),
            email=data.get("email", constants.EMPTY_VALUE),
            fullName=data.get("name", constants.EMPTY_VALUE),
            firstName=data.get("given_name", constants.EMPTY_VALUE),
            lastName=data.get("family_name", constants.EMPTY_VALUE),
            active=data.get("active", False),
            emailVerified=data.get("email_verified", False),
        )
    )


def get_auth_tokens_for_credentials(
    realm: str, payload: models.GetTokensForCredentialsPayload
) -> models.GetTokensForCredentialsResponse:
    """Gets the authorization tokens for the credentials and realm in context

    Args:
        realm (str): The realm in context
        payload (models.GetTokensForCredentialsPayload): The required payload to refresh token

    Returns:
        models.GetTokensForCredentialsResponse: The tokens data
    """
    response = api.get_auth_tokens_for_credentials(realm, payload)

    handle_error_response(response)

    data = response.json()

    return models.GetTokensForCredentialsResponse(
        data=models.GetTokensForCredentialsResponseData(
            accessToken=data.get("access_token"),
            expiresIn=data.get("expires_in"),
        )
    )


def register_new_user(
    realm: str, authorization: str, payload: models.RegisterUserPayload
) -> models.RegisterUserResponse:
    """Registers a new user

    Args:
        realm (str): The realm in context
        authorization (str): Admin authorization access token
        payload (models.RegisterUserPayload): The required payload to register an user

    Returns:
        models.RegisterUserResponse: The register user response
    """
    response = api.register_new_user(realm, authorization, payload)

    handle_error_response(response)

    return models.RegisterUserResponse(registered=True)


def login_user(
    realm: str, payload: models.LoginUserPayload
) -> models.LoginUserResponse:
    """Logins an user

    Args:
        realm (str): The realm in context
        payload (models.LoginUserPayload): The required payload to login an user

    Returns:
        models.LoginUserResponse: The login response
    """
    response = api.login_user(realm, payload)

    handle_error_response(response)

    data = response.json()

    return models.LoginUserResponse(
        data=models.LoginUserResponseData(
            accessToken=data.get("access_token"),
            refreshToken=data.get("refresh_token"),
            expiresIn=data.get("expires_in"),
            refreshExpiresIn=data.get("refresh_expires_in"),
        )
    )


def logout(realm: str, authorization: str, user_id: str) -> models.LogoutResponse:
    """Logs out an existing user

    Args:
        realm (str): The realm in context
        authorization (str): Admin authorization access token
        user_id (str): Id of the user to log out

    Returns:
        models.LogoutResponse: The response
    """
    response = api.logout(realm, authorization, user_id)

    handle_error_response(response)

    return models.LogoutResponse(loggedOut=True)


def send_reset_password_email(
    realm: str, authorization: str, user_id: str
) -> models.SendResetPasswordEmailResponse:
    """Sends an email to reset the user password

    Args:
        realm (str): The realm in context
        authorization (str): Admin authorization access token
        user_id (str): The id of the user to send the reset password email

    Returns:
        models.SendResetPasswordEmailResponse: The response
    """
    response = api.send_reset_password_email(realm, authorization, user_id)

    handle_error_response(response)

    return models.SendResetPasswordEmailResponse(emailSent=True)
