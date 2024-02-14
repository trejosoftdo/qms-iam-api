"""Helpers tests
"""

import unittest
from unittest.mock import Mock, patch
from app.helpers import validate_api_access
from app.exceptions import UNAUTHORIZED_ERROR, FORBIDDEN_ERROR


ALLOWED_KEY = "test-api-key-1"
ALLOWED_IP_ADDRESS = "10.0.0.12"
ALLOWED_KEYS = f"{ALLOWED_KEY},test-api-key-2"
ALLOWED_IP_ADDRESSES = f"{ALLOWED_IP_ADDRESS},192.0.0.100"

mock_environment = Mock(
    allowed_api_keys=ALLOWED_KEYS, allowed_ip_adresses=ALLOWED_IP_ADDRESSES
)


class HelpersTest(unittest.TestCase):
    """Helper functions tests"""

    @patch(
        "app.helpers.environment",
        mock_environment,
    )
    def test_validate_api_access_happy_path(self):
        """validate_api_access: It does not fail when providing allowed keys and ip addresses"""
        try:
            request_mock = Mock(client=Mock(host=ALLOWED_IP_ADDRESS))
            validate_api_access(request_mock, ALLOWED_KEY)
        except Exception as exc:
            assert False, f"Raised an exception {exc}"

    @patch(
        "app.helpers.environment",
        mock_environment,
    )
    def test_validate_api_access_not_allowed_key(self):
        """validate_api_access: It fails when providing a not allowed key"""
        request_mock = Mock(client=Mock(host=ALLOWED_IP_ADDRESS))
        self.assertRaises(
            UNAUTHORIZED_ERROR.__class__,
            validate_api_access,
            request_mock,
            "not-allowed-key",
        )

    @patch(
        "app.helpers.environment",
        mock_environment,
    )
    def test_validate_api_access_not_allowed_ip_address(self):
        """validate_api_access: It fails when the caller does not have an allowed ip address"""
        request_mock = Mock(client=Mock(host="127.1.2.3"))
        self.assertRaises(
            FORBIDDEN_ERROR.__class__,
            validate_api_access,
            request_mock,
            ALLOWED_KEY,
        )


if __name__ == "__main__":
    unittest.main()
