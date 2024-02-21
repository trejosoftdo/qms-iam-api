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

    Args:
        payload (models.AuthorizeDevicePayload): The required payload
        application (str, optional): The application in context

    Returns:
        models.AuthorizeDeviceResponse: Authorization information such as deviceCode,
        and userCode.
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

    Args:
        payload (models.GetTokensPayload): The required payload
        application (str, optional): The application in context

    Returns:
        models.GetTokensResponse: The authorization tokens information
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

    Args:
        payload (models.GetNewAccessTokenPayload): The required payload
        application (str, optional): The application in context

    Returns:
        models.GetNewAccessTokenResponse: The new access token information
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

    Args:
        payload (models.ValidateAccessTokenPayload): The required payload
        application (str, optional): The application in context
        authorization (str, optional): The authorization access token

    Returns:
        models.ValidateAccessTokenResponse: The new access token information
    """
    return handlers.validate_access_token(application, authorization, payload)
