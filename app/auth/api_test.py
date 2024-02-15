"""Helpers tests
"""

import unittest
from unittest.mock import Mock, patch
from urllib.parse import urlencode
from app.constants import (
    FORM_URL_ENCODED,
    TIMEOUT,
    DEVICE_TOKEN_GRANT_TYPE,
    REFRESH_TOKEN_GRANT_TYPE,
)
from .api import auth_device, get_auth_tokens, token_instrospect, get_new_access_token
from . import models
from . import constants as paths


BASE_URL = "http://base-url.test"

mock_environment = Mock(auth_api_base_url=BASE_URL)


class AuthAPITest(unittest.TestCase):
    """Auth API functions tests"""

    def setUp(self):
        self.realm = "test-realm"
        self.base_path = f"{BASE_URL}/realms/{self.realm}"
        self.common_headers = {"Content-Type": FORM_URL_ENCODED}

    @patch("app.auth.api.requests.post")
    @patch(
        "app.auth.api.environment",
        mock_environment,
    )
    def test_auth_device(self, post_mock):
        """auth_device: It can authorize a device against the external auth service as expected"""
        post_mock.return_value = Mock(status_code=200)
        data = models.AuthorizeDevicePayload(
            clientId="test-client-id",
            clientSecret="test-client-secret",
            scope="test-scope",
        )
        response = auth_device(self.realm, data)
        self.assertEqual(response, post_mock.return_value)
        post_mock.assert_called_with(
            f"{self.base_path}{paths.AUTH_DEVICE_PATH}",
            headers=self.common_headers,
            data=urlencode(
                {
                    "client_id": data.clientId,
                    "client_secret": data.clientSecret,
                    "scope": data.scope,
                }
            ),
            timeout=TIMEOUT,
        )

    @patch("app.auth.api.requests.post")
    @patch(
        "app.auth.api.environment",
        mock_environment,
    )
    def test_get_auth_tokens(self, post_mock):
        """get_auth_tokens: It can get auth tokens from the external auth service as expected"""
        post_mock.return_value = Mock(status_code=200)
        data = models.GetTokensPayload(
            clientId="test-client-id",
            clientSecret="test-client-secret",
            deviceCode="test-device-code",
        )
        response = get_auth_tokens(self.realm, data)
        self.assertEqual(response, post_mock.return_value)
        post_mock.assert_called_with(
            f"{self.base_path}{paths.AUTH_TOKENS_PATH}",
            headers=self.common_headers,
            data=urlencode(
                {
                    "device_code": data.deviceCode,
                    "grant_type": DEVICE_TOKEN_GRANT_TYPE,
                    "client_id": data.clientId,
                    "client_secret": data.clientSecret,
                }
            ),
            timeout=TIMEOUT,
        )

    @patch("app.auth.api.requests.post")
    @patch(
        "app.auth.api.environment",
        mock_environment,
    )
    def test_token_instrospect(self, post_mock):
        """token_instrospect: It can get token info from the auth service as expected"""
        post_mock.return_value = Mock(status_code=200)
        data = models.ValidateAccessTokenPayload(
            clientId="test-client-id",
            clientSecret="test-client-secret",
            expectedScope="test-scope",
        )
        token_mock = "test-token"
        response = token_instrospect(self.realm, token_mock, data)
        self.assertEqual(response, post_mock.return_value)
        post_mock.assert_called_with(
            f"{self.base_path}{paths.INSTROSPECT_PATH}",
            headers=self.common_headers,
            data=urlencode(
                {
                    "token": token_mock,
                    "client_id": data.clientId,
                    "client_secret": data.clientSecret,
                }
            ),
            timeout=TIMEOUT,
        )

    @patch("app.auth.api.requests.post")
    @patch(
        "app.auth.api.environment",
        mock_environment,
    )
    def test_get_new_access_token(self, post_mock):
        """get_new_access_token: It can get a new token from the auth service as expected"""
        post_mock.return_value = Mock(status_code=200)
        data = models.GetNewAccessTokenPayload(
            clientId="test-client-id",
            clientSecret="test-client-secret",
            refreshToken="test-refresh-token",
        )
        response = get_new_access_token(self.realm, data)
        self.assertEqual(response, post_mock.return_value)
        post_mock.assert_called_with(
            f"{self.base_path}{paths.AUTH_TOKENS_PATH}",
            headers=self.common_headers,
            data=urlencode(
                {
                    "refresh_token": data.refreshToken,
                    "grant_type": REFRESH_TOKEN_GRANT_TYPE,
                    "client_id": data.clientId,
                    "client_secret": data.clientSecret,
                }
            ),
            timeout=TIMEOUT,
        )


if __name__ == "__main__":
    unittest.main()
