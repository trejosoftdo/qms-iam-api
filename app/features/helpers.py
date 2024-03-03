"""Features helpers
"""
import time

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
