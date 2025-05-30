from behave import given, when, then

from utils.api_helper import (
    create_user, generate_token, get_all_books, get_book_by_isbn, add_books_to_user,
    update_book_for_user, delete_book_for_user
)
from utils.logger import get_logger
from utils.user_utils import generate_unique_credentials

logger = get_logger(__name__)


@given("I have a valid user and token")
def step_impl(context):
    context.username, context.password = generate_unique_credentials()
    context.user_payload = {
        "userName": context.username,
        "password": context.password
    }
    logger.info(f"Creating user with username: {context.username}")
    response = create_user(context.base_url, context.user_payload)
    logger.info(f"User creation response: {response.json()}")
    assert response.status_code == 201
    context.user_id = response.json()["userID"]

    logger.info(f"Generating token for user: {context.username}")
    token_response = generate_token(context.base_url, context.user_payload)
    logger.info(f"Token generation response: {token_response.json()}")
    assert token_response.status_code == 200
    context.token = token_response.json()["token"]


@given("I have a valid user and a book in their collection")
def step_impl(context):
    context.execute_steps("""
        Given I have a valid user and token
        When I send a POST request to add book with ISBN "9781449325862" to the user's account
        Then the response status code should be 201
    """)


@when("I send a GET request to fetch all books")
def step_impl(context):
    logger.info("Sending GET request to fetch all books")
    context.response = get_all_books(context.base_url)
    logger.debug(f"Get all books response: {context.response.status_code} - {context.response.text}")


@then("the response should contain a non-empty list of books")
def step_impl(context):
    books = context.response.json().get("books", [])
    logger.debug(f"Books received: {books}")
    assert books, f"Expected non-empty list of books. Got: {books}"


@when('I send a GET request to fetch book with ISBN "{isbn}"')
def step_impl(context, isbn):
    logger.info(f"Fetching book by ISBN: {isbn}")
    context.response = get_book_by_isbn(context.base_url, isbn)
    logger.debug(f"Get book response: {context.response.status_code} - {context.response.text}")


@then('the response should contain the book title "{title}"')
def step_impl(context, title):
    actual_title = context.response.json().get("title")
    logger.debug(f"Expected title: {title}, Actual title: {actual_title}")
    assert actual_title == title, f"Expected title '{title}', got '{actual_title}'"


@when('I send a POST request to add book with ISBN "{isbn}" to the user\'s account')
def step_impl(context, isbn):
    logger.info(f"Adding book {isbn} to user {context.user_id}")
    context.response = add_books_to_user(context.base_url, context.token, context.user_id, isbn)
    logger.debug(f"Add book response: {context.response.status_code} - {context.response.text}")


@when('I send a PUT request to replace book with ISBN "{old_isbn}" with "{new_isbn}"')
def step_impl(context, old_isbn, new_isbn):
    logger.info(f"Replacing book {old_isbn} with {new_isbn} for user {context.user_id}")
    context.response = update_book_for_user(context.base_url, context.token, context.user_id, old_isbn, new_isbn)
    logger.debug(f"Update book response: {context.response.status_code} - {context.response.text}")


@given('I have a valid user and a book with ISBN "{isbn}" in their collection')
def step_impl(context, isbn):
    context.username, context.password = generate_unique_credentials()
    context.user_payload = {
        "userName": context.username,
        "password": context.password
    }
    logger.info(f"Creating user with username: {context.username}")

    create_resp = create_user(context.base_url, context.user_payload)
    logger.info(f"User creation response: {create_resp.json()}")
    assert create_resp.status_code == 201
    context.user_id = create_resp.json()["userID"]

    logger.info(f"Generating token for user: {context.username}")
    token_resp = generate_token(context.base_url, context.user_payload)
    logger.info(f"Token generation response: {token_resp.json()}")
    assert token_resp.status_code == 200
    context.token = token_resp.json()["token"]

    logger.info(f"Adding book {isbn} to user {context.user_id}")
    add_resp = add_books_to_user(context.base_url, context.token, context.user_id, isbn)
    logger.info(f"Add book response: {add_resp.json()}")
    assert add_resp.status_code in [200, 201], f"Failed to add book. Response: {add_resp.text}"


@when('I send a DELETE request to remove book with ISBN "{isbn}"')
def step_impl(context, isbn):
    logger.info(f"Deleting book {isbn} from user {context.user_id}")
    context.response = delete_book_for_user(context.base_url, context.token, context.user_id, isbn)
    logger.debug(f"Delete book response: {context.response.status_code} - {context.response.text}")


@then('the response status code should be {expected:d}')
def step_impl(context, expected):
    actual = context.response.status_code
    logger.info(f"Asserting response status code: expected {expected}, actual {actual}")
    logger.debug(f"Full response: {context.response.text}")
    assert actual == expected, f"Expected {expected}, got {actual}. Response: {context.response.text}"
