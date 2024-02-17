"""Exceptions
"""

from fastapi import HTTPException, status
from . import constants
from . import models


INTERNAL_SERVER_ERROR = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail=models.APIResponse(
        message=constants.INTERNAL_SERVER_ERROR_MESSAGE,
        code=constants.INTERNAL_SERVER_ERROR_CODE,
        type=constants.INTERNAL_ERROR_TYPE,
    ).dict(),
)

INVALID_TOKEN_ERROR = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail=models.APIResponse(
        message=constants.INVALID_TOKEN_ERROR_MESSAGE,
        code=constants.INVALID_TOKEN_ERROR_CODE,
        type=constants.AUTHORIZATION_ERROR_TYPE,
    ).dict(),
)

FORBIDDEN_ERROR = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail=models.APIResponse(
        message=constants.FORBIDDEN_ERROR_MESSAGE,
        code=constants.FORBIDDEN_ERROR_CODE,
        type=constants.AUTHORIZATION_ERROR_TYPE,
    ).dict(),
)

UNAUTHORIZED_ERROR = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail=models.APIResponse(
        message=constants.UNAUTHORIZED_ERROR_MESSAGE,
        code=constants.UNAUTHORIZED_ERROR_CODE,
        type=constants.AUTHORIZATION_ERROR_TYPE,
    ).dict(),
)


def get_validation_error(data: dict) -> HTTPException:
    """Gets a validation error from given data

    Args:
        data (dict): error data

    Returns:
        HTTPException: 400 HTTP Exception
    """
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=models.APIResponse(
            message=data.get("error_description"),
            code=data.get("error"),
            type=constants.VALIDATION_ERROR_TYPE,
        ).dict(),
    )
