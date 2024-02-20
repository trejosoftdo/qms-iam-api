
Feature: Access tokens endpoint
    As a consumer, I want an endpoint able to get access tokens for devices

    Background:
      Given a device and user code have been obtained
      And a request url "/api/v1/auth/tokens"


    Scenario: Get access tokens pending
        Given "VALID" request json payload
        When the request sends "POST"
        Then the response status is "HTTP_400_BAD_REQUEST"
        And the response property "code" is equal to "authorization_pending"
        And the response property "type" is equal to "VALIDATION_ERROR"
        And the response property "message" is equal to "The authorization request is still pending"


    Scenario: Get access tokens success
        Given the device has been authorized
        And "VALID" request json payload
        When the request sends "POST"
        Then the response status is "HTTP_200_OK"
        And the response property "data.expiresIn" is equal to "300"
        And the response property "data.refreshExpiresIn" matches regular expression "1\d\d\d"
        And the response property "data.accessToken" matches regular expression "^[a-zA-Z0-9_=]+\.[a-zA-Z0-9_=]+\.[a-zA-Z0-9_\-\+\/=]*"
        And the response property "data.refreshToken" matches regular expression "^[a-zA-Z0-9_=]+\.[a-zA-Z0-9_=]+\.[a-zA-Z0-9_\-\+\/=]*"


    Scenario: Get access tokens validation errors
        Given "INVALID" request json payload
        When the request sends "POST"
        Then the response status is "HTTP_400_BAD_REQUEST"
        And the response property "code" is equal to "BAD_REQUEST"
        And the response property "type" is equal to "VALIDATION_ERROR"
        And the response property "message" is equal to "field required (body.deviceCode). field required (body.clientId). field required (body.clientSecret)"


    Scenario: Get access tokens with bad credentials
        Given "BAD_CREDENTIALS" request json payload
        When the request sends "POST"
        Then the response status is "HTTP_500_INTERNAL_SERVER_ERROR"
        And the response property "code" is equal to "INTERNAL_SERVER_ERROR"
        And the response property "type" is equal to "INTERNAL_ERROR"
        And the response property "message" is equal to "Internal Server Error"


    Scenario: Get access tokens  with invalid key
        Given "VALID" request json payload
        And "api_key" header is "invalid-api-key"
        When the request sends "POST"
        Then the response status is "HTTP_401_UNAUTHORIZED"
        And the response property "code" is equal to "UNAUTHORIZED"
        And the response property "type" is equal to "AUTHORIZATION_ERROR"
        And the response property "message" is equal to "Unauthorized"
