"""Background steps"""

# pylint: disable=E0611

import time
from fastapi import status
from selenium.webdriver.common.by import By
from behave import given


def should_login(driver):
    """Checks if should login to portal

    Args:
        driver (WebDriver): web driver

    Returns:
        bool: Returns true if should login
    """
    return driver.find_elements(By.CSS_SELECTOR, "#kc-form-login")


def login_to_portal(driver, verification_uri, credentials):
    """Logs in to the authorization portal

    Args:
        driver (WebDriver): web driver
        verification_uri (str): portal verification url
        credentials (dict): login credentials
    """
    driver.get(verification_uri)

    if should_login(driver):
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


@given("access token has been obtained")
def step_obtain_access_tokens(context):
    """Obtains the access tokens

    Args:
        context (Any): Test context
    """
    tokens_path = "/api/v1/auth/tokens"
    payload = context.payloads[tokens_path]["VALID"]
    response = context.client.post(
        tokens_path,
        json=payload,
        headers=context.common_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    context.data = data["data"]
    token_refresh_path = "/api/v1/auth/token/refresh"
    context.payloads[token_refresh_path]["VALID"] = {
        **context.payloads[token_refresh_path]["VALID"],
        "refreshToken": data["data"]["refreshToken"],
    }
    access_token = data["data"]["accessToken"]
    context.headers = {"authorization": f"Bearer {access_token}"}


@given("access token is invalid")
def step_set_invalid_access_tokens(context):
    """Sets an invalid access token to authorization

    Args:
        context (Any): Test context
    """
    context.headers = {"authorization": f"Bearer {context.invalid_token}"}
