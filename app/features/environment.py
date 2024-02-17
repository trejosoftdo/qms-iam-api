from behave import fixture, use_fixture
from fastapi.testclient import TestClient
from app.main import app
from app.environment import (
    test_auth_api_client_id,
    test_auth_api_client_secret,
    test_auth_api_key,
    test_auth_application,
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
def setup_payloads(context, *args, **kwargs):
    """Sets up Test Payloads"""
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
        }
    }

def before_feature(context, feature):
    """Run setup steps before running feature files"""
    use_fixture(setup_api_client, context)
    use_fixture(setup_headers, context)
    use_fixture(setup_payloads, context)
