import requests
from urllib.parse import urlencode
from .. import environment
from .. import constants
from . import models


common_headers = {
  'Content-Type': 'application/x-www-form-urlencoded'
}

def auth_device(realm: str, payload: models.AuthorizeDevicePayload) -> requests.Response:
  """Authorizes a device to a realm in context via the auth API

  Args:
    realm (str): The realm in context
    payload (str): The required payload

  Returns:
      requests.Response: The response from the auth API.
  """
  auth_device_url = f"{environment.auth_api_base_url}/realms/{realm}/protocol/openid-connect/auth/device"
  payload = urlencode({
    'client_id': payload.clientId,
    'client_secret': payload.clientSecret,
    'scope': payload.scope,
  })
  return requests.request('POST', auth_device_url, headers = common_headers, data = payload)


def get_auth_tokens(realm: str, payload: models.GetTokensPayload) -> requests.Response:
  """Gets the authorization tokens for the given device code and realm in context

  Args:
      realm (str): The realm in context
      payload (models.GetTokensPayload): The required payload to authorize

  Returns:
      requests.Response: The response from the auth API.
  """
  get_auth_tokens_url = f"{environment.auth_api_base_url}/realms/{realm}/protocol/openid-connect/token"
  payload = urlencode({
    'device_code': payload.deviceCode,
    'grant_type': constants.DEVICE_TOKEN_GRANT_TYPE,
    'client_id': payload.clientId,
    'client_secret': payload.clientSecret,
  })
  return requests.request('POST', get_auth_tokens_url, headers = common_headers, data = payload)


def token_instrospect(realm: str, access_token: str, payload: models.ValidateAccessTokenPayload) -> requests.Response:
  """Gets information such as scope and active from the given token

  Args:
      realm (str): The realm in context
      access_token (str): The token to instrospect
      payload (models.ValidateAccessTokenPayload): The required payload to intronspect the token

  Returns:
      requests.Response: The response from the auth API.
  """
  instrospect_token_url = f"{environment.auth_api_base_url}/realms/{realm}/protocol/openid-connect/token/introspect"
  payload = urlencode({
    'token': access_token,
    'client_id': payload.clientId,
    'client_secret': payload.clientSecret,
  })
  return requests.request('POST', instrospect_token_url, headers = common_headers, data = payload)


def get_new_access_token(realm: str, payload: models.GetNewAccessTokenPayload) -> requests.Response:
  """Gets a new access token

  Args:
      realm (str): The realm in context
      payload (models.GetNewAccessTokenPayload): The required payload to get the new access token

  Returns:
      requests.Response: The response from the auth API.
  """
  refresh_token_url = f"{environment.auth_api_base_url}/realms/{realm}/protocol/openid-connect/token"
  payload = urlencode({
    'refresh_token': payload.refreshToken,
    'grant_type': constants.REFRESH_TOKEN_GRANT_TYPE,
    'client_id': payload.clientId,
    'client_secret': payload.clientSecret,
  })
  return requests.request('POST', refresh_token_url, headers = common_headers, data = payload)
