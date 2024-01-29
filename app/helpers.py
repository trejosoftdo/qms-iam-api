from fastapi import Header, Request
from . import environment
from . import constants
from . import exceptions


def validate_api_access(
  request: Request,
  api_key: str = Header(..., convert_underscores = False),
):
  """Validates the access to the API

  Args:
    request (Request): incoming request
    api_key (str, optional): API Key

  Raises:
    HTTPException: Authorization error when providing an invalid api key
    HTTPException: Forbidden error when the ip addres is not an allowed one
  """
  allowed_keys = environment.allowed_api_keys.split(constants.API_KEYS_SEPARATOR) 
  allowed_adresses = environment.allowed_ip_adresses.split(constants.IP_ADDRESSES_SEPARATOR) 

  if not api_key in allowed_keys:
    raise exceptions.UNAUTHORIZED_ERROR

  if not request.client.host in allowed_adresses:
    raise exceptions.FORBIDDEN_ERROR

