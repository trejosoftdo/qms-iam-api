"""API Handlers tests
"""

import unittest
from unittest.mock import Mock, patch
from fastapi import status
from requests import Response
from .handlers import (
    authorize_device,
    get_auth_tokens,
    get_new_access_token,
    validate_access_token,
)
from . import models
from .. import exceptions


class HandlersTest(unittest.TestCase):
    """Auth Handlers functions tests"""

    def setUp(self):
        self.realm = "test-realm"
        self.access_token = "test-access-token"

    @patch("app.auth.handlers.handle_error_response")
    @patch("app.auth.api.auth_device")
    def test_authorize_device(self, auth_device_mock, handle_error_response_mock):
        """authorize_device: It can authorize a device"""
        json_data = {
            "device_code": "test-device-code",
            "user_code": "test-user-code",
            "expires_in": 1800,
            "interval": 10,
            "verification_uri_complete": "http://test-ver.test",
        }
        auth_device_mock.return_value = Mock(
            spec=Response,
            status_code=status.HTTP_200_OK,
            json=Mock(return_value=json_data),
        )
        payload = models.AuthorizeDevicePayload(
            clientId="test-client-id",
            clientSecret="test-client-secret",
            scope="test-scope",
        )
        response = authorize_device(self.realm, payload)

        self.assertEqual(response.data.deviceCode, json_data["device_code"])
        self.assertEqual(response.data.userCode, json_data["user_code"])
        self.assertEqual(response.data.expiresIn, json_data["expires_in"])
        self.assertEqual(response.data.interval, json_data["interval"])
        self.assertEqual(
            response.data.verificationURI, json_data["verification_uri_complete"]
        )
        auth_device_mock.assert_called_with(self.realm, payload)
        handle_error_response_mock.assert_called_with(auth_device_mock.return_value)

    @patch("app.auth.handlers.handle_error_response")
    @patch("app.auth.api.get_auth_tokens")
    def test_get_auth_tokens(self, get_auth_tokens_mock, handle_error_response_mock):
        """get_auth_tokens: It can retrieve access tokens"""
        json_data = {
            "access_token": self.access_token,
            "refresh_token": "test-refresh-token",
            "expires_in": 1800,
            "refresh_expires_in": 3600,
        }
        get_auth_tokens_mock.return_value = Mock(
            spec=Response,
            status_code=status.HTTP_200_OK,
            json=Mock(return_value=json_data),
        )
        payload = models.GetTokensPayload(
            clientId="test-client-id",
            clientSecret="test-client-secret",
            deviceCode="test-device-code",
        )
        response = get_auth_tokens(self.realm, payload)
        self.assertEqual(response.data.accessToken, json_data["access_token"])
        self.assertEqual(response.data.refreshToken, json_data["refresh_token"])
        self.assertEqual(response.data.expiresIn, json_data["expires_in"])
        self.assertEqual(
            response.data.refreshExpiresIn, json_data["refresh_expires_in"]
        )
        get_auth_tokens_mock.assert_called_with(self.realm, payload)
        handle_error_response_mock.assert_called_with(get_auth_tokens_mock.return_value)

    @patch("app.auth.handlers.handle_error_response")
    @patch("app.auth.api.get_new_access_token")
    def test_get_new_access_token(
        self, get_new_access_token_mock, handle_error_response_mock
    ):
        """get_new_access_token: It can get a new access token"""
        json_data = {
            "access_token": self.access_token,
            "expires_in": 1800,
        }
        get_new_access_token_mock.return_value = Mock(
            spec=Response,
            status_code=status.HTTP_200_OK,
            json=Mock(return_value=json_data),
        )
        payload = models.GetNewAccessTokenPayload(
            clientId="test-client-id",
            clientSecret="test-client-secret",
            refreshToken="test-refresh-token",
        )
        response = get_new_access_token(self.realm, payload)

        self.assertEqual(response.data.accessToken, json_data["access_token"])
        self.assertEqual(response.data.expiresIn, json_data["expires_in"])

        get_new_access_token_mock.assert_called_with(self.realm, payload)
        handle_error_response_mock.assert_called_with(
            get_new_access_token_mock.return_value
        )

    @patch("app.auth.api.token_instrospect")
    def test_validate_access_token(self, token_instrospect_mock):
        """validate_access_token: It returns valid and authorized when the token is active and have expected scope"""
        json_data = {
            "scope": "first-scope test-scope third-scope",
            "active": True,
        }
        authorization = f"Bearer {self.access_token}"
        token_instrospect_mock.return_value = Mock(
            spec=Response,
            status_code=status.HTTP_200_OK,
            json=Mock(return_value=json_data),
        )
        payload = models.ValidateAccessTokenPayload(
            clientId="test-client-id",
            clientSecret="test-client-secret",
            expectedScope="test-scope",
        )

        response = validate_access_token(self.realm, authorization, payload)

        self.assertEqual(response.data.isValid, True)
        self.assertEqual(response.data.isAuthorized, True)
        self.assertEqual(response.data.expectedScope, payload.expectedScope)

        token_instrospect_mock.assert_called_with(
            self.realm, self.access_token, payload
        )

    @patch("app.auth.api.token_instrospect")
    def test_validate_access_token_invalid(self, token_instrospect_mock):
        """validate_access_token: It returns invalid when token is not active"""
        json_data = {
            "scope": "first-scope test-scope third-scope",
            "active": False,
        }
        authorization = f"Bearer {self.access_token}"
        token_instrospect_mock.return_value = Mock(
            spec=Response,
            status_code=status.HTTP_200_OK,
            json=Mock(return_value=json_data),
        )
        payload = models.ValidateAccessTokenPayload(
            clientId="test-client-id",
            clientSecret="test-client-secret",
            expectedScope="test-scope",
        )

        response = validate_access_token(self.realm, authorization, payload)

        self.assertEqual(response.data.isValid, False)
        self.assertEqual(response.data.isAuthorized, True)
        self.assertEqual(response.data.expectedScope, payload.expectedScope)

        token_instrospect_mock.assert_called_with(
            self.realm, self.access_token, payload
        )

    @patch("app.auth.api.token_instrospect")
    def test_validate_access_token_unathorized(self, token_instrospect_mock):
        """validate_access_token: It returns unauthorized when the expected scope is not valid"""
        json_data = {
            "scope": "first-scope test-scope third-scope",
            "active": True,
        }
        authorization = f"Bearer {self.access_token}"
        token_instrospect_mock.return_value = Mock(
            spec=Response,
            status_code=status.HTTP_200_OK,
            json=Mock(return_value=json_data),
        )
        payload = models.ValidateAccessTokenPayload(
            clientId="test-client-id",
            clientSecret="test-client-secret",
            expectedScope="unknown-scope",
        )

        response = validate_access_token(self.realm, authorization, payload)

        self.assertEqual(response.data.isValid, True)
        self.assertEqual(response.data.isAuthorized, False)
        self.assertEqual(response.data.expectedScope, payload.expectedScope)

        token_instrospect_mock.assert_called_with(
            self.realm, self.access_token, payload
        )

    @patch("app.auth.api.token_instrospect")
    def test_validate_access_token_unexpected_error_handling(
        self, token_instrospect_mock
    ):
        """validate_access_token: It handles unexpected errors properly"""
        authorization = f"Bearer {self.access_token}"
        token_instrospect_mock.side_effect = Exception("Unexpected error")
        payload = models.ValidateAccessTokenPayload(
            clientId="test-client-id",
            clientSecret="test-client-secret",
            expectedScope="unknown-scope",
        )

        self.assertRaises(
            exceptions.INTERNAL_SERVER_ERROR.__class__,
            validate_access_token,
            self.realm,
            authorization,
            payload,
        )

        token_instrospect_mock.assert_called_with(
            self.realm, self.access_token, payload
        )


if __name__ == "__main__":
    unittest.main()
