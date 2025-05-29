from behave import given, when, then

from utils.api_helper import create_user, generate_token, retrieve_user
from utils.user_utils import generate_unique_credentials


@given("I generate a unique test username and password")
def step_impl(context):
    context.username, context.password = generate_unique_credentials()
    context.user_payload = {
        "userName": context.username,
        "password": context.password
    }


@when("I send a POST request to create the user")
def step_impl(context):
    context.response = create_user(context.base_url, context.user_payload)
    if context.response.status_code == 201:
        context.user_id = context.response.json().get("userID")


@when(u'I send a POST request to generate a token for the user')
def step_impl(context):
    context.response = generate_token(context.base_url, context.user_payload)
    context.token = context.response.json().get("token")


@then(u'the response status code should be 200 and contain a token')
def step_impl(context):
    assert context.response.status_code == 200, \
        f"Expected 200, got {context.response.status_code}. Response: {context.response.text}"
    assert context.token, f"Token not found in response: {context.response.json()}"


@then("the user should be retrievable by GET request")
def step_impl(context):
    context.response = retrieve_user(context.base_url, context.user_id, context.token)
    assert context.response.status_code == 200, f"Expected 200, got {context.response.status_code}. Response: {context.response.text}"
    assert context.response.json().get("username") == context.username, \
        f"Expected username '{context.username}', got '{context.response.json().get('username')}'"


@given("I generate a unique test username and an empty password")
def step_impl(context):
    context.username, _ = generate_unique_credentials()
    context.password = ""
    context.user_payload = {
        "userName": context.username,
        "password": context.password
    }


@given("I set an invalid token")
def step_impl(context):
    context.token = "invalid_token_123"


@when("I send a POST request to generate a token with invalid password")
def step_impl(context):
    payload = {
        "userName": context.username,
        "password": "WrongPassword!"
    }
    context.response = generate_token(context.base_url, payload)


@then('the response should contain "{expected_message}"')
def step_impl(context, expected_message):
    response_text = context.response.text
    assert expected_message in response_text, \
        f"Expected '{expected_message}' in response. Got: {response_text}"


@when("I send a GET request to retrieve the user")
def step_impl(context):
    context.response = retrieve_user(context.base_url, context.user_id, context.token)


@then('the response status code should be {expected:d}')
def step_impl(context, expected):
    actual = context.response.status_code
    assert actual == expected, f"Expected {expected}, got {actual}. Response: {context.response.text}"


@given("I send a POST request to create the user")
def step_impl(context):
    return context.execute_steps("When I send a POST request to create the user")


@given('I generate a unique test username and invalid password')
def step_impl(context):
    context.username, _ = generate_unique_credentials()
    context.password = "Password123"
    context.user_payload = {
        "userName": context.username,
        "password": context.password
    }


@when("I send another POST request to create the same user again")
def step_impl(context):
    context.response = create_user(context.base_url, context.user_payload)


@when("I attempt to generate a token with an empty password")
def step_impl(context):
    payload = {
        "userName": context.username,
        "password": ""
    }
    context.response = generate_token(context.base_url, payload)


@given("I generate a valid password only")
def step_impl(context):
    context.username = None
    context.password = "SecurePass_123!"


@when("I attempt to generate a token with missing username")
def step_impl(context):
    payload = {
        "password": context.password
    }
    context.response = generate_token(context.base_url, payload)
