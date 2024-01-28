from pydantic import BaseModel

class GetTokensPayload(BaseModel):
    deviceCode: str
    clientId: str
    clientSecret: str

class AuthorizeDevicePayload(BaseModel):
    clientId: str
    clientSecret: str
    scope: str

class AuthorizeDeviceResponseData(BaseModel):
    deviceCode: str
    userCode: str
    expiresIn: int
    interval: int
    verificationURI: str

class AuthorizeDeviceResponse(BaseModel):
    data: AuthorizeDeviceResponseData

class GetTokensResponseData(BaseModel):
    accessToken: str
    refreshToken: str
    expiresIn: int
    refreshExpiresIn: int

class GetTokensResponse(BaseModel):
    data: GetTokensResponseData

class GetNewAccessTokenPayload(BaseModel):
    refreshToken: str
    clientId: str
    clientSecret: str

class GetNewAccessTokenResponseData(BaseModel):
    accessToken: str
    expiresIn: int

class GetNewAccessTokenResponse(BaseModel):
    data: GetNewAccessTokenResponseData


class ValidateAccessTokenPayload(BaseModel):
    clientId: str
    clientSecret: str
    expectedScope: str

class ValidateAccessTokenResponseData(BaseModel):
    isValid: bool
    isAuthorized: bool
    expectedScope: str

class ValidateAccessTokenResponse(BaseModel):
    data: ValidateAccessTokenResponseData
