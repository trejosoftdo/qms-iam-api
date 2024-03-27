
Feature: Refresh tokens endpoint
    As a consumer, I want an endpoint able to get renew tokens

    Background:
      Given a device and user code have been obtained
      And the device has been authorized
      And access token has been obtained
      And a request url "/api/v1/auth/token/refresh"


    Scenario: Refresh access token success
        Given "VALID" request json payload
        When the request sends "POST"
        Then the response status is "HTTP_200_OK"
        And the response property "data.expiresIn" matches regular expression "\d\d\d\d"
        And the response property "data.accessToken" matches regular expression "^[a-zA-Z0-9_=]+\.[a-zA-Z0-9_=]+\.[a-zA-Z0-9_\-\+\/=]*"


    Scenario: Refresh access token validation errors
        Given "INVALID" request json payload
        When the request sends "POST"
        Then the response status is "HTTP_400_BAD_REQUEST"
        And the response property "code" is equal to "BAD_REQUEST"
        And the response property "type" is equal to "VALIDATION_ERROR"
        And the response property "message" is equal to "field required (body.refreshToken). field required (body.clientId). field required (body.clientSecret)"


    Scenario: Refresh access token with bad credentials
        Given "BAD_CREDENTIALS" request json payload
        When the request sends "POST"
        Then the response status is "HTTP_401_UNAUTHORIZED"
        And the response property "code" is equal to "UNAUTHORIZED"
        And the response property "type" is equal to "AUTHORIZATION_ERROR"
        And the response property "message" is equal to "Unauthorized"


    Scenario: Refresh access token  with invalid key
        Given "VALID" request json payload
        And "api_key" header is "invalid-api-key"
        When the request sends "POST"
        Then the response status is "HTTP_401_UNAUTHORIZED"
        And the response property "code" is equal to "UNAUTHORIZED"
        And the response property "type" is equal to "AUTHORIZATION_ERROR"
        And the response property "message" is equal to "Unauthorized"
