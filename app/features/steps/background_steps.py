"""Background steps"""

import time
from fastapi import status
from selenium.webdriver.common.by import By
from behave import given


def login_to_portal(driver, verification_uri, credentials):
    """Logs in to the authorization portal

    Args:
        driver (WebDriver): web driver
        verification_uri (str): portal verification url
        credentials (dict): login credentials
    """
    driver.get(verification_uri)
    driver.find_element(By.ID, "username").send_keys(credentials["username"])
    driver.find_element(By.ID, "password").send_keys(credentials["password"])
    driver.find_element(By.ID, "kc-login").click()


def approve(driver):
    """Approves a device code

    Args:
        driver (WebDriver): web driver
    """
    time.sleep(2)
    driver.find_element(By.ID, "kc-login").click()
    time.sleep(2)


@given("a device and user code have been obtained")
def step_obtain_device_and_user_code(context):
    """Obtains the device and user code

    Args:
        context (Any): Test context
    """
    auth_device_path = "/api/v1/auth/device"
    payload = context.payloads[auth_device_path]["VALID"]
    response = context.client.post(
        auth_device_path,
        json=payload,
        headers=context.common_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    context.data = data["data"]
    tokens_path = "/api/v1/auth/tokens"
    context.payloads[tokens_path]["VALID"] = {
        **context.payloads[tokens_path]["VALID"],
        "deviceCode": data["data"]["deviceCode"],
    }


@given("the device has been authorized")
def step_authorize_device(context):
    """Authorizes the device for the user in context

    Args:
        context (Any): Test context
    """
    login_to_portal(
        context.driver, context.data["verificationURI"], context.credentials
    )
    approve(context.driver)
