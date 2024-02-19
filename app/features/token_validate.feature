
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


    Scenario: Token validation validation errors
        Given "INVALID" request json payload
        When the request sends "POST"
        Then the response status is "HTTP_400_BAD_REQUEST"
        And the response property "code" is equal to "BAD_REQUEST"
        And the response property "type" is equal to "VALIDATION_ERROR"
        And the response property "message" is equal to "field required (body.clientId). field required (body.clientSecret). field required (body.expectedScope)"


    Scenario: Token validation with invalid scope
        Given "INVALID_SCOPE" request json payload
        When the request sends "POST"
        Then the response status is "HTTP_200_OK"
        And the response property "data.isValid" is equal to "True"
        And the response property "data.isAuthorized" is equal to "False"
        And the response property "data.expectedScope" is equal to "execute_categories"


    Scenario: Token validation with invalid access token
        Given access token is invalid
        Given "VALID" request json payload
        When the request sends "POST"
        Then the response status is "HTTP_200_OK"
        And the response property "data.isValid" is equal to "False"
        And the response property "data.isAuthorized" is equal to "False"
        And the response property "data.expectedScope" is equal to "read_categories"


    Scenario: Token validation with bad credentials
        Given "BAD_CREDENTIALS" request json payload
        When the request sends "POST"
        Then the response status is "HTTP_200_OK"
        And the response property "data.isValid" is equal to "False"
        And the response property "data.isAuthorized" is equal to "False"
        And the response property "data.expectedScope" is equal to "read_categories"


    Scenario: Token validation  with invalid key
        Given "VALID" request json payload
        And "api_key" header is "invalid-api-key"
        When the request sends "POST"
        Then the response status is "HTTP_401_UNAUTHORIZED"
        And the response property "code" is equal to "UNAUTHORIZED"
        And the response property "type" is equal to "AUTHORIZATION_ERROR"
        And the response property "message" is equal to "Unauthorized"
