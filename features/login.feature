Feature: Login API functionality

  Scenario: Successfully create a new user with valid credentials
    Given I generate a unique test username and password
    When I send a POST request to create the user
    Then the response status code should be 201
    When I send a POST request to generate a token for the user
    Then the response status code should be 200 and contain a token
    And the user should be retrievable by GET request


  Scenario: Fail to create a user with a missing password
    Given I generate a unique test username and an empty password
    When I send a POST request to create the user
    Then the response status code should be 400
    And the response should contain "{"code":"1200","message":"UserName and Password required."}"


  Scenario: Fail to generate token with invalid password
    Given I generate a unique test username and password
    And I send a POST request to create the user
    When I send a POST request to generate a token with invalid password
    Then the response status code should be 200
    And the response should contain "User authorization failed"

  Scenario: Fail to retrieve user with invalid token
    Given I generate a unique test username and password
    And I send a POST request to create the user
    And I set an invalid token
    When I send a GET request to retrieve the user
    Then the response status code should be 401
    And the response should contain "User not authorized!"

  Scenario: Fail to create a user with a password missing non-alphanumeric character
    Given I generate a unique test username and invalid password
    When I send a POST request to create the user
    Then the response status code should be 400
    And the response should contain "Passwords must have at least one non alphanumeric character"

  Scenario: Fail to create a user with an already existing username
    Given I generate a unique test username and password
    And I send a POST request to create the user
    When I send another POST request to create the same user again
    Then the response status code should be 406
    And the response should contain "User exists!"

  Scenario: Fail to generate a token with missing password
    Given I generate a unique test username and password
    And I send a POST request to create the user
    When I attempt to generate a token with an empty password
    Then the response status code should be 400
    And the response should contain "UserName and Password required."

  Scenario: Fail to generate a token with missing username
    Given I generate a valid password only
    When I attempt to generate a token with missing username
    Then the response status code should be 400
    And the response should contain "UserName and Password required."
