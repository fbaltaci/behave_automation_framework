Feature: Login API functionality

  Scenario Outline: Successfully create a new user
    Given I have new user credentials "<username>" and "<password>"
    When I send a POST request to create the user
    Then the response status code should be 201 or 406

    Examples:
      | username         | password         |
      | test_user_123    | TestUser_123!    |
      | fb_test_user_456 | FbUser456$secure |
