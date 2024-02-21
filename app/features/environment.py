"""Integration tests environment setup"""

from behave import fixture, use_fixture
from fastapi.testclient import TestClient
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from app.main import app
from app.environment import (
    test_auth_api_client_id,
    test_auth_api_client_secret,
    test_auth_api_key,
    test_auth_application,
    test_auth_username,
    test_auth_password,
)
from app.features import constants

# pylint: disable=W0613


@fixture
def setup_web_driver(context, *args, **kwargs):
    """Sets up the web driver"""
    options = Options()
    options.add_argument(constants.DRIVER_HEADLESS_MODE_OPTION)
    options.add_argument(constants.DRIVER_NO_SANDBOX_OPTION)
    options.add_argument(constants.DRIVER_DISABLE_DEV_SHM_OPTION)
    context.driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )


@fixture
def setup_api_client(context, *args, **kwargs):
    """Sets up Test API Client"""
    context.client = TestClient(app)


@fixture
def setup_headers(context, *args, **kwargs):
    """Sets up Test headers"""
    context.common_headers = {
        "application": test_auth_application,
        "api_key": test_auth_api_key,
    }


@fixture
def setup_user_credentials(context, *args, **kwargs):
    """Sets up user credentials"""
    context.credentials = {
        "username": test_auth_username,
        "password": test_auth_password,
    }


@fixture
def setup_payloads(context, *args, **kwargs):
    """Sets up Test Payloads"""
    api_valid_credentials = {
        "clientId": test_auth_api_client_id,
        "clientSecret": test_auth_api_client_secret,
    }
    api_invalid_credentials = {
        "clientId": constants.TEST_BAD_CLIENT_ID,
        "clientSecret": constants.TEST_BAD_CLIENT_SECRET,
    }
    context.invalid_token = constants.INVALID_TOKEN
    context.payloads = {
        constants.AUTH_DEVICE_PATH: {
            "VALID": {
                **api_valid_credentials,
                "scope": constants.TEST_VALID_SCOPE,
            },
            "INVALID": {},
            "BAD_CREDENTIALS": {
                **api_invalid_credentials,
                "scope": constants.TEST_VALID_SCOPE,
            },
        },
        constants.AUTH_TOKENS_PATH: {
            "VALID": {**api_valid_credentials},
            "INVALID": {},
            "BAD_CREDENTIALS": {
                **api_invalid_credentials,
                "deviceCode": constants.TEST_INVALID_DEVICE_CODE,
            },
        },
        constants.AUTH_REFRESH_TOKEN_PATH: {
            "VALID": {
                **api_valid_credentials,
            },
            "INVALID": {},
            "BAD_CREDENTIALS": {
                **api_invalid_credentials,
                "refreshToken": constants.TEST_REFRESH_TOKEN,
            },
        },
        constants.AUTH_VALIDATE_TOKEN_PATH: {
            "VALID": {
                **api_valid_credentials,
                "expectedScope": constants.TEST_VALID_SCOPE,
            },
            "INVALID_SCOPE": {
                **api_valid_credentials,
                "expectedScope": constants.TEST_INVALID_SCOPE,
            },
            "INVALID": {},
            "BAD_CREDENTIALS": {
                **api_invalid_credentials,
                "expectedScope": constants.TEST_VALID_SCOPE,
            },
        },
    }


def before_feature(context, feature):
    """Run setup steps before running feature files"""
    use_fixture(setup_api_client, context)
    use_fixture(setup_headers, context)
    use_fixture(setup_payloads, context)
    use_fixture(setup_web_driver, context)
    use_fixture(setup_user_credentials, context)
