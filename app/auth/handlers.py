from fastapi import HTTPException
from . import models
from . import api


def authorize_device(realm: str) -> models.AuthorizeDeviceResponseData:
  """Authorizes a device to a realm in context via the auth API

  Args:
      realm (str): the realm in context

  Returns:
      models.AuthorizeDeviceResponseData: Authorization information such as deviceCode, and userCode.
  """
  response = api.auth_device(realm)
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


def get_auth_tokens(realm: str, device_code: str) -> models.GetTokensResponse:
  """Gets the authorization tokens for the given device code and realm in context

  Args:
      realm (str): The realm in context
      device_code (str): The device code to authorize

  Raises:
      HTTPException: When validation errors are encountered.
      HTTPException: When unexpected errors are encountered

  Returns:
      models.GetTokensResponse: The authorization tokens information
  """
  response = api.get_auth_tokens(realm, device_code)
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

def get_new_access_token(realm: str, refresh_token: str) -> models.GetNewAccessTokenResponse:
  """Gets a new authorization token for the given refresh token and realm in context

  Args:
      realm (str): The realm in context
      refresh_token (str): The refresh token

  Raises:
      HTTPException: When validation errors are encountered.
      HTTPException: When unexpected errors are encountered

  Returns:
      models.GetNewAccessTokenResponse: The new access token data
  """
  response = api.get_new_access_token(realm, refresh_token)
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
