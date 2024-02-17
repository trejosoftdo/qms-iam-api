import re
from fastapi import status
from behave import given, when, then


def find(data, element):
    keys = element.split(".")
    result = data
    for key in keys:
        result = result[key]
    return result


@given('a request url "{path}"')
def step_set_request_path(context, path):
    context.path = path


@given('"{payload_name}" request json payload')
def step_set_payload_name(context, payload_name):
    context.payload_name = payload_name


@given('"{name}" header is "{value}"')
def step_set_header_value(context, name, value):
    if not hasattr(context, 'headers'):
        setattr(context, 'headers', {})

    context.headers[name] = value


@when('the request sends "{method}"')
def step_send_request(context, method):
    if not hasattr(context, 'headers'):
        setattr(context, 'headers', {})

    func = getattr(context.client, method.lower())
    payload = context.payloads[context.path][context.payload_name]

    context.response = func(
        context.path,
        json=payload,
        headers={**context.common_headers, **context.headers},
    )


@then('the response status is "{status_name}"')
def step_check_response_status(context, status_name):
    # print(context.response.status_code)
    # print(getattr(status, status_name))
    # print(context.response.json())
    assert context.response.status_code == getattr(status, status_name)


@then('the response property "{property_path}" is equal to "{value}"')
def step_check_response_property(context, property_path, value):
    data = context.response.json()
    assert str(find(data, property_path)) == value


@then('the response property "{property_path}" matches regular expression "{pattern}"')
def step_check_response_property_matches_pattern(context, property_path, pattern):
    data = context.response.json()
    value = str(find(data, property_path))
    match = re.search(pattern, value)
    assert match != None
