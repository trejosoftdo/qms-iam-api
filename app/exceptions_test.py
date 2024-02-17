"""Helpers tests
"""

import unittest
from fastapi import HTTPException, status
from app.exceptions import get_validation_error
from . import models
from . import constants


class ExceptionsHelpersTests(unittest.TestCase):
    """Exceptions helpers tests"""

    def test_get_validation_error(self):
        """get_validation_error: It maps the error properly from error code and description"""
        data = {
            "error": "TEST_ERROR_CODE",
            "error_description": "Test error description",
        }
        result = get_validation_error(data)
        self.assertIsInstance(result, HTTPException)
        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsInstance(result.detail, models.APIResponse)
        self.assertEqual(result.detail.message, data["error_description"])
        self.assertEqual(result.detail.code, data["error"])
        self.assertEqual(result.detail.type, constants.VALIDATION_ERROR_TYPE)


if __name__ == "__main__":
    unittest.main()
