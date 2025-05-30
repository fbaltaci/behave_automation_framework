from behave import given, when, then

from utils.api_helper import create_user, generate_token, retrieve_user
from utils.logger import get_logger
from utils.user_utils import generate_unique_credentials

logger = get_logger(__name__)


@given("I generate a unique test username and password")
def i_generate_unique_credentials(context):
    context.username, context.password = generate_unique_credentials()
    context.user_payload = {
        "userName": context.username,
        "password": context.password
    }


@when("I send a POST request to create the user")
def i_send_post_request_to_create_user(context):
    context.response = create_user(context.base_url, context.user_payload)
    if context.response.status_code == 201:
        context.user_id = context.response.json().get("userID")


@when(u'I send a POST request to generate a token for the user')
def i_send_post_request_to_generate_token(context):
    context.response = generate_token(context.base_url, context.user_payload)
    context.token = context.response.json().get("token")


@then(u'the response status code should be 200 and contain a token')
def the_response_status_code_should_be_200_and_contain_a_token(context):
    assert context.response.status_code == 200, \
        f"Expected 200, got {context.response.status_code}. Response: {context.response.text}"
    assert context.token, f"Token not found in response: {context.response.json()}"


@then("the user should be retrievable by GET request")
def the_user_should_be_retrievable_by_get_request(context):
    context.response = retrieve_user(context.base_url, context.user_id, context.token)
    assert context.response.status_code == 200, f"Expected 200, got {context.response.status_code}. Response: {context.response.text}"
    assert context.response.json().get("username") == context.username, \
        f"Expected username '{context.username}', got '{context.response.json().get('username')}'"


@given("I generate a unique test username and an empty password")
def i_generate_unique_credentials_with_empty_password(context):
    context.username, _ = generate_unique_credentials()
    context.password = ""
    context.user_payload = {
        "userName": context.username,
        "password": context.password
    }


@given("I set an invalid token")
def i_set_an_invalid_token(context):
    context.token = "invalid_token_123"


@when("I send a POST request to generate a token with invalid password")
def i_send_post_request_to_generate_token_with_invalid_password(context):
    payload = {
        "userName": context.username,
        "password": "WrongPassword!"
    }
    context.response = generate_token(context.base_url, payload)


@then('the response should contain "{expected_message}"')
def the_response_should_contain(context, expected_message):
    response_text = context.response.text
    assert expected_message in response_text, \
        f"Expected '{expected_message}' in response. Got: {response_text}"


@when("I send a GET request to retrieve the user")
def i_send_get_request_to_retrieve_user(context):
    context.response = retrieve_user(context.base_url, context.user_id, context.token)


@then('the response status code should be {expected:d}')
def the_response_status_code_should_be(context, expected):
    actual = context.response.status_code
    assert actual == expected, f"Expected {expected}, got {actual}. Response: {context.response.text}"


@given("I send a POST request to create the user")
def i_send_post_request_to_create_user(context):
    return context.execute_steps("When I send a POST request to create the user")


@given('I generate a unique test username and invalid password')
def i_generate_unique_credentials_with_invalid_password(context):
    context.username, _ = generate_unique_credentials()
    context.password = "Password123"
    context.user_payload = {
        "userName": context.username,
        "password": context.password
    }


@when("I send another POST request to create the same user again")
def i_send_another_post_request_to_create_the_same_user_again(context):
    context.response = create_user(context.base_url, context.user_payload)


@when("I attempt to generate a token with an empty password")
def i_attempt_to_generate_a_token_with_an_empty_password(context):
    payload = {
        "userName": context.username,
        "password": ""
    }
    context.response = generate_token(context.base_url, payload)


@given("I generate a valid password only")
def i_generate_a_valid_password_only(context):
    context.username = None
    context.password = "SecurePass_123!"


@when("I attempt to generate a token with missing username")
def i_attempt_to_generate_a_token_with_missing_username(context):
    payload = {
        "password": context.password
    }
    context.response = generate_token(context.base_url, payload)
