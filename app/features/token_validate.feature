
Feature: Token validation endpoint
    As a consumer, I want an endpoint able to get validate tokens

    Background:
      Given a device and user code have been obtained
      And the device has been authorized
      And access token has been obtained
      And a request url "/api/v1/auth/token/validate"


    Scenario: Token validation success
        Given "VALID" request json payload
        When the request sends "POST"
        Then the response status is "HTTP_200_OK"
        And the response property "data.isValid" is equal to "True"
        And the response property "data.isAuthorized" is equal to "True"
        And the response property "data.expectedScope" is equal to "read_categories"
