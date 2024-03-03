
Feature: Register new user endpoint
    As a consumer, I want an endpoint able to register a new user

    Background:
      Given a request url "/api/v1/auth/register"

    Scenario: Register new user sucesss
        Given an admin access token has been obtained
        And "VALID" request json payload
        When the request sends "POST"
        Then the response status is "HTTP_200_OK"
        And the response property "registered" is equal to "True"


    Scenario: Register new user validation errors
        Given an admin access token has been obtained
        And "INVALID" request json payload
        When the request sends "POST"
        Then the response status is "HTTP_400_BAD_REQUEST"
        And the response property "code" is equal to "BAD_REQUEST"
        And the response property "type" is equal to "VALIDATION_ERROR"
        And the response property "message" is equal to "field required (body.username). field required (body.firstName). field required (body.lastName). field required (body.email). field required (body.password)"

    Scenario: Register new user with access token
        Given access token is invalid
        Given "VALID" request json payload
        When the request sends "POST"
        Then the response status is "HTTP_500_INTERNAL_SERVER_ERROR"
        And the response property "code" is equal to "INTERNAL_SERVER_ERROR"
        And the response property "type" is equal to "INTERNAL_ERROR"
        And the response property "message" is equal to "Internal Server Error"


    Scenario: Register new user  with invalid key
        Given an admin access token has been obtained
        AND "VALID" request json payload
        And "api_key" header is "invalid-api-key"
        When the request sends "POST"
        Then the response status is "HTTP_401_UNAUTHORIZED"
        And the response property "code" is equal to "UNAUTHORIZED"
        And the response property "type" is equal to "AUTHORIZATION_ERROR"
        And the response property "message" is equal to "Unauthorized"
