"""Auth API constants
"""

TAGS = ["auth"]

# Operation Ids
AUTHORIZE_DEVICE_OPERATION_ID = "authorizeDevice"
GET_AUTH_TOKENS_OPERATION_ID = "getAuthTokens"
GET_NEW_ACCESS_TOKEN_OPERATION_ID = "getNewAccessToken"
VALIDATE_ACCESS_TOKEN_OPERATION_ID = "validateAccessToken"
TOKENS_FOR_CREDENTIALS_OPERATION_ID="getAuthTokensForCredentials"
REGISTER_USER_OPERATION_ID = "registerUser"
LOGIN_USER_OPERATION_ID = "loginUser"
GET_USER_BASIC_DATA_OPERATION_ID="getUserBasicData"
LOGOUT_OPERATION_ID="logout"
SEND_RESET_PASSWORD_EMAIL="sendResetPasswordEmail"

# External API paths
AUTH_DEVICE_PATH = "/protocol/openid-connect/auth/device"
AUTH_TOKENS_PATH = "/protocol/openid-connect/token"
INSTROSPECT_PATH = "/protocol/openid-connect/token/introspect"
AUTH_USERS_PATH = "/users"
REALMS_PATH = "/realms/"
ADMIN_PATH = "/admin"
AUTH_RESET_PASSWORD_EMAIL = "/reset-password-email"

# Route paths
DEVICE_ROUTE_PATH = "/device"
TOKENS_ROUTE_PATH = "/tokens"
TOKENS_FOR_CREDENTIALS_ROUTE_PATH = "/tokens/for-credentials"
TOKEN_REFRESH_ROUTE_PATH = "/token/refresh"
TOKEN_VALIDATE_ROUTE_PATH = "/token/validate"
REGISTER_ROUTE_PATH = "/register"
LOGIN_ROUTE_PATH = "/login"
AUTH_LOGOUT_PATH = "/logout"
USER_BASIC_DATA_PATH="/user-basic-data"
