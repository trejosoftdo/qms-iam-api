"""API Router tests
"""

import unittest
from unittest.mock import patch
from fastapi import status
from fastapi.testclient import TestClient
from .. import main, constants
from . import models
from . import constants as auth_constants


class RouterTest(unittest.TestCase):
    """Auth Router functions tests"""

    def setUp(self):
        self.client = TestClient(main.app)
        self.application = "test-application"
        self.authorization = "Bearer test-token"
        self.api_key = "test-api-key"
        self.host = "testclient"
        self.headers = {
            "application": self.application,
            "authorization": self.authorization,
            "api_key": self.api_key,
        }

    @patch("app.helpers.environment")
    @patch("app.auth.handlers.authorize_device")
    def test_authorize_device(self, auth_device_mock, environment_mock):
        """authorize_device: It can authorize a device"""
        environment_mock.allowed_api_keys = self.api_key
        environment_mock.allowed_ip_adresses = self.host

        auth_device_mock.return_value = models.AuthorizeDeviceResponse(
            data=models.AuthorizeDeviceResponseData(
                deviceCode="test-device-code",
                userCode="test-user-code",
                expiresIn=1800,
                interval=10,
                verificationURI="http://test-ver.test",
            ),
        )
        payload = models.AuthorizeDevicePayload(
            clientId="test-client-id",
            clientSecret="test-client-secret",
            scope="test-scope",
        )

        response = self.client.post(
            f"{constants.AUTH_ROUTE_PREFIX}/device",
            headers=self.headers,
            json=payload.dict(),
        )
        self.assertEqual(response.json(), auth_device_mock.return_value)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        auth_device_mock.assert_called_with(self.application, payload)

    @patch("app.helpers.environment")
    @patch("app.auth.handlers.get_auth_tokens")
    def test_get_auth_tokens(self, get_auth_tokens_mock, environment_mock):
        """get_auth_tokens: It can retrieve access tokens"""
        environment_mock.allowed_api_keys = self.api_key
        environment_mock.allowed_ip_adresses = self.host

        get_auth_tokens_mock.return_value = models.GetTokensResponse(
            data=models.GetTokensResponseData(
                accessToken="test-access-token",
                refreshToken="test-refresh-token",
                expiresIn=1800,
                refreshExpiresIn=36000,
            ),
        )
        payload = models.GetTokensPayload(
            clientId="test-client-id",
            clientSecret="test-client-secret",
            deviceCode="test-device-code",
        )
        response = self.client.post(
            f"{constants.AUTH_ROUTE_PREFIX}/tokens",
            headers=self.headers,
            json=payload.dict(),
        )
        self.assertEqual(response.json(), get_auth_tokens_mock.return_value)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        get_auth_tokens_mock.assert_called_with(self.application, payload)

    @patch("app.helpers.environment")
    @patch("app.auth.handlers.get_new_access_token")
    def test_get_new_access_token(self, get_new_access_token_mock, environment_mock):
        """get_new_access_token: It can get a new access token"""
        environment_mock.allowed_api_keys = self.api_key
        environment_mock.allowed_ip_adresses = self.host

        get_new_access_token_mock.return_value = models.GetNewAccessTokenResponse(
            data=models.GetNewAccessTokenResponseData(
                accessToken="test-access-token",
                expiresIn=1800,
            ),
        )
        payload = models.GetNewAccessTokenPayload(
            clientId="test-client-id",
            clientSecret="test-client-secret",
            refreshToken="test-refresh-token",
        )
        response = self.client.post(
            f"{constants.AUTH_ROUTE_PREFIX}/token/refresh",
            headers=self.headers,
            json=payload.dict(),
        )
        self.assertEqual(response.json(), get_new_access_token_mock.return_value)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        get_new_access_token_mock.assert_called_with(self.application, payload)

    @patch("app.helpers.environment")
    @patch("app.auth.handlers.validate_access_token")
    def test_validate_access_token(self, validate_access_token_mock, environment_mock):
        """get_new_access_token: It can get a new access token"""
        environment_mock.allowed_api_keys = self.api_key
        environment_mock.allowed_ip_adresses = self.host

        validate_access_token_mock.return_value = models.ValidateAccessTokenResponse(
            data=models.ValidateAccessTokenResponseData(
                isValid=True,
                isAuthorized=True,
                expectedScope="test-expected-scope",
            ),
        )
        payload = models.ValidateAccessTokenPayload(
            clientId="test-client-id",
            clientSecret="test-client-secret",
            expectedScope="test-scope",
        )
        response = self.client.post(
            f"{constants.AUTH_ROUTE_PREFIX}/token/validate",
            headers=self.headers,
            json=payload.dict(),
        )
        self.assertEqual(response.json(), validate_access_token_mock.return_value)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        validate_access_token_mock.assert_called_with(
            self.application, self.authorization, payload
        )

    @patch("app.helpers.environment")
    @patch("app.auth.handlers.get_auth_tokens_for_credentials")
    def test_get_auth_tokens_for_credentials(
        self, get_auth_tokens_for_credentials_mock, environment_mock
    ):
        """get_auth_tokens_for_credentials: It can get access token for a given credentials"""
        environment_mock.allowed_api_keys = self.api_key
        environment_mock.allowed_ip_adresses = self.host

        get_auth_tokens_for_credentials_mock.return_value = (
            models.GetTokensForCredentialsResponse(
                data=models.GetTokensForCredentialsResponseData(
                    accessToken="test-token",
                    expiresIn=1234,
                ),
            )
        )
        payload = models.GetTokensForCredentialsPayload(
            clientId="test-client-id",
            clientSecret="test-client-secret",
        )
        response = self.client.post(
            f"{constants.AUTH_ROUTE_PREFIX}{auth_constants.TOKENS_FOR_CREDENTIALS_ROUTE_PATH}",
            headers=self.headers,
            json=payload.dict(),
        )
        self.assertEqual(
            response.json(), get_auth_tokens_for_credentials_mock.return_value
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        get_auth_tokens_for_credentials_mock.assert_called_with(
            self.application, payload
        )

    @patch("app.helpers.environment")
    @patch("app.auth.handlers.register_new_user")
    def test_register_new_user(self, register_new_user_mock, environment_mock):
        """register_new_user: It can register a new user"""
        environment_mock.allowed_api_keys = self.api_key
        environment_mock.allowed_ip_adresses = self.host

        register_new_user_mock.return_value = models.RegisterUserResponse(
            registered=True
        )
        payload = models.RegisterUserPayload(
            username="test-user-name",
            firstName="John",
            lastName="Doe",
            email="john@doe.com",
            password="test-pass!",
        )
        response = self.client.post(
            f"{constants.AUTH_ROUTE_PREFIX}{auth_constants.REGISTER_ROUTE_PATH}",
            headers=self.headers,
            json=payload.dict(),
        )
        self.assertEqual(response.json(), register_new_user_mock.return_value)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        register_new_user_mock.assert_called_with(
            self.application, self.authorization, payload
        )

    @patch("app.helpers.environment")
    @patch("app.auth.handlers.login_user")
    def test_login_user(self, login_user_mock, environment_mock):
        """login_user: It can register a new user"""
        environment_mock.allowed_api_keys = self.api_key
        environment_mock.allowed_ip_adresses = self.host

        login_user_mock.return_value = models.LoginUserResponse(
            data=models.LoginUserResponseData(
                accessToken="test-access-token",
                refreshToken="test-refresh-token",
                expiresIn=100,
                refreshExpiresIn=3000,
            )
        )
        payload = models.LoginUserPayload(
            clientId="test-client-id",
            clientSecret="test-client-secret",
            username="test-username",
            password="test-password!",
            scope="test-scope",
        )
        response = self.client.post(
            f"{constants.AUTH_ROUTE_PREFIX}{auth_constants.LOGIN_ROUTE_PATH}",
            headers=self.headers,
            json=payload.dict(),
        )
        self.assertEqual(response.json(), login_user_mock.return_value)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        login_user_mock.assert_called_with(
            self.application, payload
        )


if __name__ == "__main__":
    unittest.main()
