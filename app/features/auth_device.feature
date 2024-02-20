
Feature: Authorize device endpoint
    As a consumer, I want an endpoint able to authorize devices

    Background:
        Given a request url "/api/v1/auth/device"

    Scenario: Authorize a device success
        Given "VALID" request json payload
        When the request sends "POST"
        Then the response status is "HTTP_200_OK"
        And the response property "data.expiresIn" is equal to "600"
        And the response property "data.interval" is equal to "5"
        And the response property "data.userCode" matches regular expression "^\w\w\w\w-\w\w\w\w$"
        And the response property "data.deviceCode" matches regular expression "^[\w-]+$"
        And the response property "data.verificationURI" matches regular expression "^(http|https):\/\/([\w.-]+)(\.[\w.-]+)+([\/\w\.-]*)*\/?"


    Scenario: Authorize a device validation errors
        Given "INVALID" request json payload
        When the request sends "POST"
        Then the response status is "HTTP_400_BAD_REQUEST"
        And the response property "code" is equal to "BAD_REQUEST"
        And the response property "type" is equal to "VALIDATION_ERROR"
        And the response property "message" is equal to "field required (body.clientId). field required (body.clientSecret). field required (body.scope)"


    Scenario: Authorize a device with bad credentials
        Given "BAD_CREDENTIALS" request json payload
        When the request sends "POST"
        Then the response status is "HTTP_500_INTERNAL_SERVER_ERROR"
        And the response property "code" is equal to "INTERNAL_SERVER_ERROR"
        And the response property "type" is equal to "INTERNAL_ERROR"
        And the response property "message" is equal to "Internal Server Error"


    Scenario: Authorize a device with invalid key
        Given "VALID" request json payload
        And "api_key" header is "invalid-api-key"
        When the request sends "POST"
        Then the response status is "HTTP_401_UNAUTHORIZED"
        And the response property "code" is equal to "UNAUTHORIZED"
        And the response property "type" is equal to "AUTHORIZATION_ERROR"
        And the response property "message" is equal to "Unauthorized"
