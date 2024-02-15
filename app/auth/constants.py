"""Auth API constants
"""

TAGS = ["auth"]

# Operation Ids
AUTHORIZE_DEVICE_OPERATION_ID = "authorizeDevice"
GET_AUTH_TOKENS_OPERATION_ID = "getAuthTokens"
GET_NEW_ACCESS_TOKEN_OPERATION_ID = "getNewAccessToken"
VALIDATE_ACCESS_TOKEN_OPERATION_ID = "validateAccessToken"

AUTH_DEVICE_PATH = "/protocol/openid-connect/auth/device"
AUTH_TOKENS_PATH = "/protocol/openid-connect/token"
INSTROSPECT_PATH = "/protocol/openid-connect/token/introspect"
