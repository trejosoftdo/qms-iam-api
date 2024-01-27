from fastapi import HTTPException
from . import constants


INTERNAL_SERVER_ERROR = HTTPException(
  status_code = constants.INTERNAL_SERVER_ERROR_CODE,
  detail = constants.INTERNAL_SERVER_ERROR_MESSAGE,
)

INVALID_TOKEN_ERROR = HTTPException(
  status_code = constants.INVALID_TOKEN_ERROR_CODE,
  detail = constants.INVALID_TOKEN_ERROR_MESSAGE,
)

FORBIDDEN_ERROR = HTTPException(
  status_code = constants.FORBIDDEN_ERROR_CODE,
  detail = constants.FORBIDDEN_ERROR_MESSAGE,
)

