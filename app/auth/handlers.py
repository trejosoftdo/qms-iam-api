from fastapi import HTTPException
from . import models
from . import api
from .. import constants
from .. import exceptions


def authorize_device(realm: str, payload: models.AuthorizeDevicePayload) -> models.AuthorizeDeviceResponseData:
  """Authorizes a device to a realm in context via the auth API

  Args:
    realm (str): the realm in context
    payload (models.AuthorizeDevicePayload): the required payload

  Returns:
      models.AuthorizeDeviceResponseData: Authorization information such as deviceCode, and userCode.
  """
  response = api.auth_device(realm, payload)
  data = response.json()
  return models.AuthorizeDeviceResponse(
    data = models.AuthorizeDeviceResponseData(
      deviceCode = data.get('device_code'),
      userCode = data.get('user_code'),
      expiresIn = data.get('expires_in'),
      interval = data.get('interval'),
      verificationURI = data.get('verification_uri_complete'),
    )
  )

def get_auth_tokens(realm: str, payload: models.GetTokensPayload) -> models.GetTokensResponse:
  """Gets the authorization tokens for the given device code and realm in context

  Args:
      realm (str): The realm in context
      payload (models.GetTokensPayload): The required payload

  Raises:
      HTTPException: When validation errors are encountered.
      HTTPException: When unexpected errors are encountered

  Returns:
      models.GetTokensResponse: The authorization tokens information
  """
  response = api.get_auth_tokens(realm, payload)
  data = response.json()
  
  if (response.status_code == 400):
    raise HTTPException(
      status_code = 400,
      detail = {
        'message': data.get('error_description'),
        'code': data.get('error'),
      },
    )
  
  if response.status_code > 400:
    raise HTTPException(
      status_code = 500,
      detail = {
        'message': 'Unexpected error',
        'code': 'INTERNAL_ERROR',
      },
    )

  return models.GetTokensResponse(
    data = models.GetTokensResponseData(
      accessToken = data.get('access_token'),
      refreshToken = data.get('refresh_token'),
      expiresIn = data.get('expires_in'),
      refreshExpiresIn = data.get('refresh_expires_in'),
    )
  )

def get_new_access_token(realm: str, payload: models.GetNewAccessTokenPayload) -> models.GetNewAccessTokenResponse:
  """Gets a new authorization token for the given refresh token and realm in context

  Args:
      realm (str): The realm in context
      payload (models.GetNewAccessTokenPayload): The required payload to refresh token

  Raises:
      HTTPException: When validation errors are encountered.
      HTTPException: When unexpected errors are encountered

  Returns:
      models.GetNewAccessTokenResponse: The new access token data
  """
  response = api.get_new_access_token(realm, payload)
  data = response.json()
  
  if (response.status_code == 400):
    raise HTTPException(
      status_code = 400,
      detail = {
        'message': data.get('error_description'),
        'code': data.get('error'),
      },
    )
  
  if response.status_code > 400:
    raise HTTPException(
      status_code = 500,
      detail = {
        'message': 'Unexpected error',
        'code': 'INTERNAL_ERROR',
      },
    )

  return models.GetNewAccessTokenResponse(
    data = models.GetNewAccessTokenResponseData(
      accessToken = data.get('access_token'),
      expiresIn = data.get('expires_in'),
    )
  )

def validate_access_token(realm: str, authorization: str, payload: models.ValidateAccessTokenPayload) -> models.ValidateAccessTokenResponse:
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
  access_token = authorization.replace(constants.BEARER_PORTION, constants.EMPTY_VALUE)

  try:
    response = api.token_instrospect(
      realm,
      access_token,
      payload,
    )
    data = response.json()
    is_valid = data.get(constants.ACTIVE_PROPERTY) == True
    scopes = data.get(constants.SCOPE_PROPERTY, constants.EMPTY_VALUE).split(constants.SCOPES_SEPARATOR)
    is_authorized = payload.expectedScope in scopes
  except:
    raise exceptions.INTERNAL_SERVER_ERROR

  if not is_valid:
    raise exceptions.INVALID_TOKEN_ERROR

  if not is_authorized:
    raise exceptions.FORBIDDEN_ERROR
  
  return models.ValidateAccessTokenResponse(
    data = models.ValidateAccessTokenResponseData(
      isValid = is_valid,
      isAuthorized = is_authorized,
      expectedScope = payload.expectedScope
    )
  )
