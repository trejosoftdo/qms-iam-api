"""Helpers tests
"""

import unittest
from unittest.mock import Mock, patch
from .api import auth_device
from . import models
from app.constants import FORM_URL_ENCODED, TIMEOUT


BASE_URL = "http://base-url.test"

mock_environment = Mock(auth_api_base_url=BASE_URL)


class AuthAPITest(unittest.TestCase):
    """Auth API functions tests"""

    def setUp(self):
        self.realm = "test-realm"

    @patch("app.auth.api.requests.post")
    @patch(
        "app.auth.api.environment",
        mock_environment,
    )
    def test_auth_device(self, post_mock):
        """auth_device: It can authorize a device against the external auth service as expected"""
        post_mock.return_value = Mock(status_code=200)
        payload = models.AuthorizeDevicePayload(
            clientId="test-client-id",
            clientSecret="test-client-secret",
            scope="test-scope",
        )
        response = auth_device(self.realm, payload)
        self.assertEqual(response, post_mock.return_value)
        post_mock.assert_called_with(
            f"{mock_environment.auth_api_base_url}/realms/{self.realm}/protocol/openid-connect/auth/device",
            headers={"Content-Type": FORM_URL_ENCODED},
            data=f"client_id={payload.clientId}&client_secret={payload.clientSecret}&scope={payload.scope}",
            timeout=TIMEOUT,
        )


if __name__ == "__main__":
    unittest.main()
