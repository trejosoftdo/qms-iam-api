"""API general steps"""

# pylint: disable=E0611

import re
from fastapi import status
from behave import given, when, then


def find(data, path):
    """_summary_

    Args:
        data (dict): source data
        path (str): value path

    Returns:
        Any: found value
    """
    keys = path.split(".")
    result = data
    for key in keys:
        result = result[key]
    return result


@given('a request url "{path}"')
def step_set_request_path(context, path):
    """Sets the request path

    Args:
        context (Any): Test context
        path (string): endpoint path
    """
    context.path = path


@given('"{payload_name}" request json payload')
def step_set_payload_name(context, payload_name):
    """Sets the request payload

    Args:
        context (Any): Test context
        payload_name (string): payload name
    """
    context.payload = context.payloads[context.path][payload_name]

@given('"{name}" header is "{value}"')
def step_set_header_value(context, name, value):
    """Sets the a header value

    Args:
        context (Any): Test context
        name (string): header name
        value (string): header value
    """
    if not hasattr(context, "headers"):
        setattr(context, "headers", {})

    context.headers[name] = value


@when('the request sends "{method}"')
def step_send_request(context, method):
    """Send a request to the path in context 
       using the chosen payload as body

    Args:
        context (Any): Test context
        method (string): Request method (POST, GET, PUT, ...)
    """
    if not hasattr(context, "headers"):
        setattr(context, "headers", {})

    func = getattr(context.client, method.lower())

    context.response = func(
        context.path,
        json=context.payload,
        headers={**context.common_headers, **context.headers},
    )


@then('the response status is "{status_name}"')
def step_check_response_status(context, status_name):
    """Checks the response status

    Args:
        context (Any): Test context
        status_name (string): Status name
    """
    # print(context.response.status_code)
    # print(getattr(status, status_name))
    # print(context.response.json())
    assert context.response.status_code == getattr(status, status_name)


@then('the response property "{property_path}" is equal to "{value}"')
def step_check_response_property(context, property_path, value):
    """Checks the value of a response property

    Args:
        context (Any): Test context
        property_path (string): Path of the property
        value (string): expected value
    """
    data = context.response.json()
    assert str(find(data, property_path)) == value


@then('the response property "{property_path}" matches regular expression "{pattern}"')
def step_check_response_property_matches_pattern(context, property_path, pattern):
    """Checks if a value in a response matches a regex pattern

    Args:
        context (Any): Test context
        property_path (string): Path of the property
        pattern (string): expected regex pattern
    """
    data = context.response.json()
    value = str(find(data, property_path))
    match = re.search(pattern, value)
    assert match is not None
