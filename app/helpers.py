from fastapi import Header
# from . import constants
from . import exceptions


def validate_api_access(
  api_key: str = Header(..., convert_underscores = False),
):
  """Validates the access to the API

  Args:
    api_key (str, optional): API Key

  Raises:
    HTTPException: Authorization error when being unautorized.
  """
  print(api_key)
  # TODO: implement validation logic
  is_valid = True

  if not is_valid:
    raise exceptions.UNAUTHORIZED_ERROR

