"""API responses descriptions"""

from fastapi import status
from app import constants
from app.models import APIResponse


responses_descriptions = {
    status.HTTP_400_BAD_REQUEST: {
        "model": APIResponse,
        "description": constants.HTTP_400_DESCRIPTION,
    },
    status.HTTP_401_UNAUTHORIZED: {
        "model": APIResponse,
        "description": constants.HTTP_401_DESCRIPTION,
    },
    status.HTTP_403_FORBIDDEN: {
        "model": APIResponse,
        "description": constants.HTTP_403_DESCRIPTION,
    },
    status.HTTP_404_NOT_FOUND: {
        "model": APIResponse,
        "description": constants.HTTP_404_DESCRIPTION,
    },
    status.HTTP_422_UNPROCESSABLE_ENTITY: {
        "model": APIResponse,
        "description": constants.HTTP_422_DESCRIPTION,
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "model": APIResponse,
        "description": constants.HTTP_500_DESCRIPTION,
    },
}
