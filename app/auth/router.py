"""Auth API router
"""

from fastapi import APIRouter, Depends, Header
from . import handlers
from . import models
from . import constants
from .. import helpers
from .. import responses


router = APIRouter()


@router.post(
    constants.DEVICE_ROUTE_PATH,
    dependencies=[Depends(helpers.validate_api_access)],
    tags=constants.TAGS,
    operation_id=constants.AUTHORIZE_DEVICE_OPERATION_ID,
    response_model=models.AuthorizeDeviceResponse,
    responses=responses.responses_descriptions,
)
def authorize_device(
    payload: models.AuthorizeDevicePayload,
    application: str = Header(..., convert_underscores=False),
) -> models.AuthorizeDeviceResponse:
    """Authorize a device to an application in context
    """
    return handlers.authorize_device(application, payload)


@router.post(
    constants.TOKENS_ROUTE_PATH,
    dependencies=[Depends(helpers.validate_api_access)],
    tags=constants.TAGS,
    operation_id=constants.GET_AUTH_TOKENS_OPERATION_ID,
    response_model=models.GetTokensResponse,
    responses=responses.responses_descriptions,
)
async def get_auth_tokens(
    payload: models.GetTokensPayload,
    application: str = Header(..., convert_underscores=False),
) -> models.GetTokensResponse:
    """Gets the authorization tokens for the given device code and application in context
    """
    return handlers.get_auth_tokens(application, payload)


@router.post(
    constants.TOKEN_REFRESH_ROUTE_PATH,
    dependencies=[Depends(helpers.validate_api_access)],
    tags=constants.TAGS,
    operation_id=constants.GET_NEW_ACCESS_TOKEN_OPERATION_ID,
    response_model=models.GetNewAccessTokenResponse,
    responses=responses.responses_descriptions,
)
async def get_new_access_token(
    payload: models.GetNewAccessTokenPayload,
    application: str = Header(..., convert_underscores=False),
) -> models.GetNewAccessTokenResponse:
    """Gets a new access token for the given refresh token and application in context
    """
    return handlers.get_new_access_token(application, payload)


@router.post(
    constants.TOKEN_VALIDATE_ROUTE_PATH,
    dependencies=[Depends(helpers.validate_api_access)],
    tags=constants.TAGS,
    operation_id=constants.VALIDATE_ACCESS_TOKEN_OPERATION_ID,
    response_model=models.ValidateAccessTokenResponse,
    responses=responses.responses_descriptions,
)
async def validate_access_token(
    payload: models.ValidateAccessTokenPayload,
    application: str = Header(..., convert_underscores=False),
    authorization: str = Header(..., convert_underscores=False),
) -> models.ValidateAccessTokenResponse:
    """Validates a token checking if it has not expired and has the required scope
    """
    return handlers.validate_access_token(application, authorization, payload)


@router.post(
    constants.USER_BASIC_DATA_PATH,
    dependencies=[Depends(helpers.validate_api_access)],
    tags=constants.TAGS,
    operation_id=constants.GET_USER_BASIC_DATA_OPERATION_ID,
    response_model=models.UserBasicDataResponse,
    responses=responses.responses_descriptions,
)
async def get_user_basic_data(
    payload: models.UserBasicDataPayload,
    application: str = Header(..., convert_underscores=False),
    authorization: str = Header(..., convert_underscores=False),
) -> models.UserBasicDataResponse:
    """Gets the user basic data for the authorization token"""
    return handlers.get_user_basic_data(application, authorization, payload)


@router.post(
    constants.TOKENS_FOR_CREDENTIALS_ROUTE_PATH,
    dependencies=[Depends(helpers.validate_api_access)],
    tags=constants.TAGS,
    operation_id=constants.TOKENS_FOR_CREDENTIALS_OPERATION_ID,
    response_model=models.GetTokensForCredentialsResponse,
    responses=responses.responses_descriptions,
)
def get_auth_tokens_for_credentials(
    payload: models.GetTokensForCredentialsPayload,
    application: str = Header(..., convert_underscores=False),
) -> models.GetTokensForCredentialsResponse:
    """Gets the authorization tokens for the credentials and realm in context"""
    return handlers.get_auth_tokens_for_credentials(application, payload)


@router.post(
    constants.REGISTER_ROUTE_PATH,
    dependencies=[Depends(helpers.validate_api_access)],
    tags=constants.TAGS,
    operation_id=constants.REGISTER_USER_OPERATION_ID,
    response_model=models.RegisterUserResponse,
    responses=responses.responses_descriptions,
)
def register_new_user(
    payload: models.RegisterUserPayload,
    application: str = Header(..., convert_underscores=False),
    authorization: str = Header(..., convert_underscores=False),
) -> models.RegisterUserResponse:
    """Registers a new user"""
    return handlers.register_new_user(application, authorization, payload)


@router.post(
    constants.LOGIN_ROUTE_PATH,
    dependencies=[Depends(helpers.validate_api_access)],
    tags=constants.TAGS,
    operation_id=constants.LOGIN_USER_OPERATION_ID,
    response_model=models.LoginUserResponse,
    responses=responses.responses_descriptions,
)
def login_user(
    payload: models.LoginUserPayload,
    application: str = Header(..., convert_underscores=False),
) -> models.LoginUserResponse:
    """Logs in an user"""
    return handlers.login_user(application, payload)


@router.post(
    "/{user_id}/logout",
    dependencies=[Depends(helpers.validate_api_access)],
    tags=constants.TAGS,
    operation_id=constants.LOGOUT_OPERATION_ID,
    response_model=models.LogoutResponse,
    responses=responses.responses_descriptions,
)
async def logout(
    user_id: str,
    application: str = Header(..., convert_underscores=False),
    authorization: str = Header(..., convert_underscores=False),
) -> models.LogoutResponse:
    """Logs out an existing user"""
    return handlers.logout(application, authorization, user_id)


@router.put(
    "/{user_id}/reset-password-email",
    dependencies=[Depends(helpers.validate_api_access)],
    tags=constants.TAGS,
    operation_id=constants.SEND_RESET_PASSWORD_EMAIL,
    response_model=models.SendResetPasswordEmailResponse,
    responses=responses.responses_descriptions,
)
async def send_reset_password_email(
    user_id: str,
    application: str = Header(..., convert_underscores=False),
    authorization: str = Header(..., convert_underscores=False),
) -> models.SendResetPasswordEmailResponse:
    """Sends an email to reset the user password"""
    return handlers.send_reset_password_email(application, authorization, user_id)
