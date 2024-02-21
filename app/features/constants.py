"""Features constants"""

# pylint: disable=C0301

INVALID_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJUZXN0IEpXVCBCdWlsZGVyIiwiaWF0IjoxNzA4MzQ1NTUwLCJleHAiOjE3Mzk4ODE1NTAsImF1ZCI6Ind3dy5leGFtcGxlLmNvbSIsInN1YiI6Impkb2VAZXhhbXBsZS5jb20iLCJHaXZlbk5hbWUiOiJKb2huIiwiU3VybmFtZSI6IkRvZSIsIkVtYWlsIjoiamRvZUBleGFtcGxlLmNvbSIsIlJvbGUiOlsiVGVzdGVyIiwiUHJvamVjdCB0ZXN0ZXIiXX0.YeFRs0nkqBthQ-xhXSnP032CInfL3vRuRPSqWm9Ii2Q"
TEST_VALID_SCOPE = "read_categories"
TEST_INVALID_SCOPE = "execute_categories"
TEST_INVALID_DEVICE_CODE = "test-code"
TEST_REFRESH_TOKEN = "test-refresh-token"
TEST_BAD_CLIENT_ID = "bad-client-id"
TEST_BAD_CLIENT_SECRET = "bad-client-secret"

# Paths
AUTH_DEVICE_PATH = "/api/v1/auth/device"
AUTH_TOKENS_PATH = "/api/v1/auth/tokens"
AUTH_REFRESH_TOKEN_PATH = "/api/v1/auth/token/refresh"
AUTH_VALIDATE_TOKEN_PATH = "/api/v1/auth/token/validate"

# Driver options
DRIVER_HEADLESS_MODE_OPTION = "--headless"
DRIVER_NO_SANDBOX_OPTION = "--no-sandbox"
DRIVER_DISABLE_DEV_SHM_OPTION = "--disable-dev-shm-usage"

# Ids and selectors
LOGIN_FORM_SELECTOR = "#kc-form-login"
USERNAME_ID = "username"
PASSWORD_ID = "password"
LOGIN_ID = "kc-login"
APPROVE_ID = "kc-login"
