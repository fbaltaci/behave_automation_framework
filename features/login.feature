Feature: Login API functionality

  Scenario: Successfully create a new user with valid credentials
    Given I generate a unique test username and password
    When I send a POST request to create the user
    Then the response status code should be 201
    When I send a POST request to generate a token for the user
    Then the response status code should be 200 and contain a token
    And the user should be retrievable by GET request
