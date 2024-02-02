"""Environment variables
"""

import os
from dotenv import load_dotenv
from . import constants

load_dotenv()

auth_api_base_url = os.getenv(constants.AUTH_API_BASE_URL_ENV_NAME)
allowed_ip_adresses = os.getenv(constants.AUTH_ALLOWED_IP_ADDRESSES_ENV_NAME)
allowed_api_keys = os.getenv(
    constants.AUTH_ALLOWED_API_KEYS_ENV_NAME, constants.EMPTY_VALUE
)
