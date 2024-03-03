"""Environment variables
"""

import os
from dotenv import load_dotenv
from app import constants

load_dotenv()

auth_api_base_url = os.getenv(constants.AUTH_API_BASE_URL_ENV_NAME)
allowed_ip_adresses = os.getenv(constants.AUTH_ALLOWED_IP_ADDRESSES_ENV_NAME)
allowed_api_keys = os.getenv(
    constants.AUTH_ALLOWED_API_KEYS_ENV_NAME, constants.EMPTY_VALUE
)

test_auth_api_key = os.getenv(constants.TEST_AUTH_API_KEY_ENV_NAME)
test_auth_api_client_id = os.getenv(constants.TEST_AUTH_API_CLIENT_ID_ENV_NAME)
test_auth_api_client_secret = os.getenv(constants.TEST_AUTH_API_CLIENT_SECRET_ENV_NAME)

test_auth_admin_api_client_id = os.getenv(constants.TEST_AUTH_ADMIN_API_CLIENT_ID_ENV_NAME)
test_auth_admin_api_client_secret = os.getenv(constants.TEST_AUTH_ADMIN_API_CLIENT_SECRET_ENV_NAME)

test_auth_application = os.getenv(constants.TEST_AUTH_APPLICATION_ENV_NAME)
test_auth_username = os.getenv(constants.TEST_AUTH_USERNAME_ENV_NAME)
test_auth_password = os.getenv(constants.TEST_AUTH_PASSWORD_ENV_NAME)
