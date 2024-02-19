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

# pylint: disable=W0613
# pylint: disable=C0301


@fixture
def setup_web_driver(context, *args, **kwargs):
    """Sets up the web driver"""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
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
    context.invalid_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJUZXN0IEpXVCBCdWlsZGVyIiwiaWF0IjoxNzA4MzQ1NTUwLCJleHAiOjE3Mzk4ODE1NTAsImF1ZCI6Ind3dy5leGFtcGxlLmNvbSIsInN1YiI6Impkb2VAZXhhbXBsZS5jb20iLCJHaXZlbk5hbWUiOiJKb2huIiwiU3VybmFtZSI6IkRvZSIsIkVtYWlsIjoiamRvZUBleGFtcGxlLmNvbSIsIlJvbGUiOlsiVGVzdGVyIiwiUHJvamVjdCB0ZXN0ZXIiXX0.YeFRs0nkqBthQ-xhXSnP032CInfL3vRuRPSqWm9Ii2Q"
    context.payloads = {
        "/api/v1/auth/device": {
            "VALID": {
                "clientId": test_auth_api_client_id,
                "clientSecret": test_auth_api_client_secret,
                "scope": "read_categories",
            },
            "INVALID": {},
            "BAD_CREDENTIALS": {
                "clientId": "bad-client-id",
                "clientSecret": "bad-client-secret",
                "scope": "read_categories",
            },
        },
        "/api/v1/auth/tokens": {
            "VALID": {
                "clientId": test_auth_api_client_id,
                "clientSecret": test_auth_api_client_secret,
            },
            "INVALID": {},
            "BAD_CREDENTIALS": {
                "clientId": "bad-client-id",
                "clientSecret": "bad-client-secret",
                "deviceCode": "test-code",
            },
        },
        "/api/v1/auth/token/refresh": {
            "VALID": {
                "clientId": test_auth_api_client_id,
                "clientSecret": test_auth_api_client_secret,
            },
            "INVALID": {},
            "BAD_CREDENTIALS": {
                "clientId": "bad-client-id",
                "clientSecret": "bad-client-secret",
                "refreshToken": "test-refresh-token",
            },
        },
        "/api/v1/auth/token/validate": {
            "VALID": {
                "clientId": test_auth_api_client_id,
                "clientSecret": test_auth_api_client_secret,
                "expectedScope": "read_categories",
            },
            "INVALID_SCOPE": {
                "clientId": test_auth_api_client_id,
                "clientSecret": test_auth_api_client_secret,
                "expectedScope": "execute_categories",
            },
            "INVALID": {},
            "BAD_CREDENTIALS": {
                "clientId": "bad-client-id",
                "clientSecret": "bad-client-secret",
                "expectedScope": "read_categories",
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
