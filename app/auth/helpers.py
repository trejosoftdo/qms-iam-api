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

    if response.status_code > status.HTTP_400_BAD_REQUEST:
        raise exceptions.INTERNAL_SERVER_ERROR
