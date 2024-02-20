"""API responses descriptions"""

from app import constants
from app.models import APIResponse


responses_descriptions = {
    400: {
        "model": APIResponse,
        "description": constants.HTTP_400_DESCRIPTION,
    },
    401: {
        "model": APIResponse,
        "description": constants.HTTP_401_DESCRIPTION,
    },
    403: {
        "model": APIResponse,
        "description": constants.HTTP_403_DESCRIPTION,
    },
    404: {
        "model": APIResponse,
        "description": constants.HTTP_404_DESCRIPTION,
    },
    422: {
        "model": APIResponse,
        "description": constants.HTTP_422_DESCRIPTION,
    },
    500: {
        "model": APIResponse,
        "description": constants.HTTP_500_DESCRIPTION,
    },
}
