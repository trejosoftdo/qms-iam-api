"""Auth API models
"""

from pydantic import BaseModel


class GetTokensPayload(BaseModel):
    """Get Tokens Payload data

    Args:
        BaseModel (class): Base model class
    """

    deviceCode: str
    clientId: str
    clientSecret: str


class AuthorizeDevicePayload(BaseModel):
    """Authorize Device Payload data

    Args:
        BaseModel (class): Base model class
    """

    clientId: str
    clientSecret: str
    scope: str


class AuthorizeDeviceResponseData(BaseModel):
    """Authorize Device Response data

    Args:
        BaseModel (class): Base model class
    """

    deviceCode: str
    userCode: str
    expiresIn: int
    interval: int
    verificationURI: str


class AuthorizeDeviceResponse(BaseModel):
    """Authorize Device Response

    Args:
        BaseModel (class): Base model class
    """

    data: AuthorizeDeviceResponseData


class GetTokensResponseData(BaseModel):
    """Get Tokens Response data

    Args:
        BaseModel (class): Base model class
    """

    accessToken: str
    refreshToken: str
    expiresIn: int
    refreshExpiresIn: int


class GetTokensResponse(BaseModel):
    """Get Tokens Response

    Args:
        BaseModel (class): Base model class
    """

    data: GetTokensResponseData


class GetNewAccessTokenPayload(BaseModel):
    """Get New Access Token Payload data

    Args:
        BaseModel (class): Base model class
    """

    refreshToken: str
    clientId: str
    clientSecret: str


class GetNewAccessTokenResponseData(BaseModel):
    """Get New Access Token Response data

    Args:
        BaseModel (class): Base model class
    """

    accessToken: str
    expiresIn: int


class GetNewAccessTokenResponse(BaseModel):
    """Get New Access Token Response

    Args:
        BaseModel (class): Base model class
    """

    data: GetNewAccessTokenResponseData


class ValidateAccessTokenPayload(BaseModel):
    """Validate Access Token Payload

    Args:
        BaseModel (class): Base model class
    """

    clientId: str
    clientSecret: str
    expectedScope: str


class ValidateAccessTokenResponseData(BaseModel):
    """Validate Access Token Response data

    Args:
        BaseModel (class): Base model class
    """

    isValid: bool
    isAuthorized: bool
    expectedScope: str


class ValidateAccessTokenResponse(BaseModel):
    """Validate Access Token Response

    Args:
        BaseModel (class): Base model class
    """

    data: ValidateAccessTokenResponseData
