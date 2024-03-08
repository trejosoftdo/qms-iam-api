"""Auth API helpers
"""

from fastapi import status
from requests import Response
from .. import exceptions


def handle_error_response(response: Response) -> None:
    """Handles error responses

    Args:
        response (Response): The API response

    Raises:
        HTTPException(status_code=400): validation error
        HTTPException(status_code=500): Internal server error
    """
    if response.status_code == status.HTTP_400_BAD_REQUEST:
        data = response.json()
        raise exceptions.get_validation_error(data)

    if response.status_code == status.HTTP_401_UNAUTHORIZED:
        raise exceptions.UNAUTHORIZED_ERROR

    if response.status_code == status.HTTP_403_FORBIDDEN:
        raise exceptions.FORBIDDEN_ERROR

    if response.status_code == status.HTTP_409_CONFLICT:
        raise exceptions.CONFLICT_ERROR

    if response.status_code > status.HTTP_403_FORBIDDEN:
        raise exceptions.INTERNAL_SERVER_ERROR
