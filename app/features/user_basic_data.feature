
Feature: User basic data endpoint
    As a consumer, I want an endpoint able to get the basic data of an user

    Background:
      Given an admin access token has been obtained
      And an user has been registered
      And the user has obtained access token
      And the user access token it is used
      And a request url "/api/v1/auth/user-basic-data"


    Scenario: User basic data sucesss
        Given "VALID" request json payload
        When the request sends "POST"
        Then the response status is "HTTP_200_OK"
        And the response property "data.username" matches regular expression "test_.+"
        And the response property "data.email" matches regular expression "test_.+"
        And the response property "data.fullName" matches regular expression "Test .+"
        And the response property "data.firstName" matches regular expression "Test .+"
        And the response property "data.lastName" matches regular expression "Automation .+"
        And the response property "data.active" is equal to "True"
        And the response property "data.emailVerified" is equal to "False"


    Scenario: User basic data with invalid key
        Given "VALID" request json payload
        And "api_key" header is "invalid-api-key"
        When the request sends "POST"
        Then the response status is "HTTP_401_UNAUTHORIZED"
        And the response property "code" is equal to "UNAUTHORIZED"
        And the response property "type" is equal to "AUTHORIZATION_ERROR"
        And the response property "message" is equal to "Unauthorized"


    Scenario: User basic data with invalid access token
        Given access token is invalid
        And "VALID" request json payload
        When the request sends "POST"
        Then the response status is "HTTP_401_UNAUTHORIZED"
        And the response property "code" is equal to "UNAUTHORIZED"
        And the response property "type" is equal to "AUTHORIZATION_ERROR"
        And the response property "message" is equal to "Unauthorized"