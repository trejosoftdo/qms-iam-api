"""Features helpers
"""

import time
import requests
from app.features import constants
from app.environment import (
    auth_api_base_url,
    test_auth_admin_api_client_id,
    test_auth_admin_api_client_secret,
    test_auth_application,
)


def get_user_register_payload():
    """Gets the user register payload"""
    test_id = time.time()
    return {
        "username": f"test_automation_user_{test_id}",
        "firstName": f"Test {test_id}",
        "lastName": f"Automation User {test_id}",
        "email": f"test_automation_user_{test_id}@test.com",
        "password": "testpass{test_id}",
    }


def delete_test_user(user_id, access_token):
    """Deletes a test user"""
    requests.delete(
        f"{auth_api_base_url}/admin/realms/{test_auth_application}/users/{user_id}",
        headers={"authorization": f"Bearer {access_token}"},
        timeout=10
    )


def delete_test_users(context):
    """Deletes the test users"""
    response = context.client.post(
        constants.AUTH_TOKENS_FOR_CREDENCIALS_PATH,
        json={
            "clientId": test_auth_admin_api_client_id,
            "clientSecret": test_auth_admin_api_client_secret,
            "scope": "email profile",
        },
        headers={
            **context.common_headers,
        },
        timeout=10
    )
    data = response.json()
    access_token = data["data"]["accessToken"]
    response = requests.get(
        f"{auth_api_base_url}/admin/realms/{test_auth_application}/users",
        headers={"authorization": f"Bearer {access_token}"},
        timeout=10
    )
    data = response.json()

    for user in data:
        if user["username"].startswith("test_automation_user_"):
            delete_test_user(user["id"], access_token)
