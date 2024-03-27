
Feature: Reset password email endpoint
    As a consumer, I want an endpoint able to send reset password email to users

    Background:
      Given an admin access token has been obtained
      And an user has been registered
      And the user has obtained access token
      And a request url "/api/v1/auth/:user/reset-password-email"


    Scenario: Reset password email failure
        Given "INVALID" request json payload
        When the request sends "PUT"
        Then the response status is "HTTP_500_INTERNAL_SERVER_ERROR"