
Feature: Login user endpoint
    As a consumer, I want an endpoint able to login existing users

    Background:
      Given an admin access token has been obtained
      And an user has been registered
      And a request url "/api/v1/auth/login"

    Scenario: Login user sucesss
        Given an admin access token has been obtained
        And "VALID" request json payload
        When the request sends "POST"
        Then the response status is "HTTP_200_OK"
        And the response property "data.expiresIn" matches regular expression "\d\d\d\d"
        And the response property "data.accessToken" matches regular expression "^[a-zA-Z0-9_=]+\.[a-zA-Z0-9_=]+\.[a-zA-Z0-9_\-\+\/=]*"


    Scenario: Login user validation errors
        Given an admin access token has been obtained
        And "INVALID" request json payload
        When the request sends "POST"
        Then the response status is "HTTP_400_BAD_REQUEST"
        And the response property "code" is equal to "BAD_REQUEST"
        And the response property "type" is equal to "VALIDATION_ERROR"
        And the response property "message" is equal to "field required (body.clientId). field required (body.clientSecret). field required (body.username). field required (body.password). field required (body.scope)"


    Scenario: Login user with invalid key
        Given an admin access token has been obtained
        And "VALID" request json payload
        And "api_key" header is "invalid-api-key"
        When the request sends "POST"
        Then the response status is "HTTP_401_UNAUTHORIZED"
        And the response property "code" is equal to "UNAUTHORIZED"
        And the response property "type" is equal to "AUTHORIZATION_ERROR"
        And the response property "message" is equal to "Unauthorized"


    Scenario: Login non existing user
        Given "NON_EXISTING" request json payload
        When the request sends "POST"
        Then the response status is "HTTP_401_UNAUTHORIZED"
        And the response property "code" is equal to "UNAUTHORIZED"
        And the response property "type" is equal to "AUTHORIZATION_ERROR"
        And the response property "message" is equal to "Unauthorized"
