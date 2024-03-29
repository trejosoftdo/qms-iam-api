"""Background steps"""

# pylint: disable=E0611

import time
from fastapi import status
from selenium.webdriver.common.by import By
from behave import given
import jwt
from app.features import constants
from app.features.helpers import get_user_register_payload


def should_login(driver):
    """Checks if should login to portal

    Args:
        driver (WebDriver): web driver

    Returns:
        bool: Returns true if should login
    """
    return driver.find_elements(By.CSS_SELECTOR, constants.LOGIN_FORM_SELECTOR)


def login_to_portal(driver, verification_uri, credentials):
    """Logs in to the authorization portal

    Args:
        driver (WebDriver): web driver
        verification_uri (str): portal verification url
        credentials (dict): login credentials
    """
    driver.get(verification_uri)

    if should_login(driver):
        driver.find_element(By.ID, constants.USERNAME_ID).send_keys(
            credentials["username"]
        )
        driver.find_element(By.ID, constants.PASSWORD_ID).send_keys(
            credentials["password"]
        )
        driver.find_element(By.ID, constants.LOGIN_ID).click()


def approve(driver):
    """Approves a device code

    Args:
        driver (WebDriver): web driver
    """
    time.sleep(2)
    driver.find_element(By.ID, constants.APPROVE_ID).click()
    time.sleep(2)


@given("a device and user code have been obtained")
def step_obtain_device_and_user_code(context):
    """Obtains the device and user code

    Args:
        context (Any): Test context
    """
    response = context.client.post(
        constants.AUTH_DEVICE_PATH,
        json=context.payloads[constants.AUTH_DEVICE_PATH]["VALID"],
        headers=context.common_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    context.data = data["data"]
    context.payloads[constants.AUTH_TOKENS_PATH]["VALID"] = {
        **context.payloads[constants.AUTH_TOKENS_PATH]["VALID"],
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
    response = context.client.post(
        constants.AUTH_TOKENS_PATH,
        json=context.payloads[constants.AUTH_TOKENS_PATH]["VALID"],
        headers=context.common_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    context.data = data["data"]
    context.payloads[constants.AUTH_REFRESH_TOKEN_PATH]["VALID"] = {
        **context.payloads[constants.AUTH_REFRESH_TOKEN_PATH]["VALID"],
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


@given("an admin access token has been obtained")
def step_obtain_admin_access_tokens(context):
    """Obtains an admin access tokens

    Args:
        context (Any): Test context
    """
    response = context.client.post(
        constants.AUTH_TOKENS_FOR_CREDENCIALS_PATH,
        json=context.payloads[constants.AUTH_TOKENS_FOR_CREDENCIALS_PATH]["VALID"],
        headers=context.common_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    access_token = data["data"]["accessToken"]
    context.headers = {"authorization": f"Bearer {access_token}"}
    context.admin_access_token = access_token


@given("an user has been registered")
def step_register_user(context):
    """Registers a new user

    Args:
        context (Any): Test context
    """
    register_payload = get_user_register_payload()
    context.payloads[constants.AUTH_REGISTER_USER_PATH]["VALID"] = register_payload
    response = context.client.post(
        constants.AUTH_REGISTER_USER_PATH,
        json=register_payload,
        headers={
            **context.common_headers,
            **context.headers,
        }
    )
    assert response.status_code == status.HTTP_200_OK
    context.payloads[constants.AUTH_LOGIN_USER_PATH]["VALID"] = {
        **context.payloads[constants.AUTH_LOGIN_USER_PATH]["VALID"],
        "username": register_payload["username"],
        "password": register_payload["password"],
    }


@given("the user has obtained access token")
def step_obtain_user_access_tokens(context):
    """Obtains an user access tokens

    Args:
        context (Any): Test context
    """
    response = context.client.post(
        constants.AUTH_LOGIN_USER_PATH,
        json=context.payloads[constants.AUTH_LOGIN_USER_PATH]["VALID"],
        headers=context.common_headers,
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    token = data.get('data', {})['accessToken']
    decoded_data = jwt.decode(token, options={"verify_signature": False})
    context.user_logout_path = f"/api/v1/auth/{decoded_data['sub']}/logout"
    reset_email_path = f"/api/v1/auth/reset-password-email?email={decoded_data['email']}"
    context.user_reset_password_email_path = reset_email_path
    context.user_access_token = token


@given("the user access token it is used")
def step_use_user_access_token(context):
    """Uses the user obtained access token

    Args:
        context (Any): Test context
    """
    context.headers = {"authorization": f"Bearer {context.user_access_token}"}
