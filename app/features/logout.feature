
Feature: Logout user endpoint
    As a consumer, I want an endpoint able to log out existing users

    Background:
      Given an admin access token has been obtained
      And an user has been registered
      And the user has obtained access token
      And a request url "/api/v1/auth/:user/logout"


    Scenario: Logout user sucesss
        Given "VALID" request json payload
        When the request sends "POST"
        Then the response status is "HTTP_200_OK"
        And the response property "loggedOut" is equal to "True"


    Scenario: Logout user with invalid key
        Given "VALID" request json payload
        And "api_key" header is "invalid-api-key"
        When the request sends "POST"
        Then the response status is "HTTP_401_UNAUTHORIZED"
        And the response property "code" is equal to "UNAUTHORIZED"
        And the response property "type" is equal to "AUTHORIZATION_ERROR"
        And the response property "message" is equal to "Unauthorized"


    Scenario: Logout user with invalid access token
        Given access token is invalid
        And "VALID" request json payload
        When the request sends "POST"
        Then the response status is "HTTP_401_UNAUTHORIZED"
        And the response property "code" is equal to "UNAUTHORIZED"
        And the response property "type" is equal to "AUTHORIZATION_ERROR"
        And the response property "message" is equal to "Unauthorized"