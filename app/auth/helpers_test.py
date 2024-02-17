"""API Handlers tests
"""

import unittest
from unittest.mock import Mock, patch
from fastapi import status, HTTPException
from requests import Response
from .helpers import handle_error_response


class AuthHelpersTest(unittest.TestCase):
    """Auth helpers functions tests"""

    def setUp(self):
        self.data = {"title": "Test title"}

    @patch("app.auth.helpers.exceptions.get_validation_error")
    def test_handle_error_response_not_error(self, get_validation_error_mock):
        """handle_error_response: It does not fail when the status code is not an error"""
        response_mock = Mock(
            spec=Response,
            status_code=status.HTTP_200_OK,
            json=Mock(return_value=self.data),
        )
        self.assertIsNone(handle_error_response(response_mock))
        get_validation_error_mock.assert_not_called()

    @patch("app.auth.helpers.exceptions.get_validation_error")
    def test_handle_error_response_validation_error(self, get_validation_error_mock):
        """handle_error_response: it returns a validation error when the error status is 400"""
        get_validation_error_mock.return_value = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
        )
        response_mock = Mock(
            spec=Response,
            status_code=status.HTTP_400_BAD_REQUEST,
            json=Mock(return_value=self.data),
        )
        self.assertRaises(HTTPException, handle_error_response, response_mock)
        get_validation_error_mock.assert_called_with(self.data)

    @patch("app.auth.helpers.exceptions.get_validation_error")
    def test_handle_error_response_unexpected_error(self, get_validation_error_mock):
        """handle_error_response: it returns an internal error when status is greater than 400"""
        response_mock = Mock(
            spec=Response,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            json=Mock(return_value=self.data),
        )
        self.assertRaises(HTTPException, handle_error_response, response_mock)
        get_validation_error_mock.assert_not_called()
