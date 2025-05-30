from behave import given, when, then

from utils.api_helper import (
    get_all_books, get_book_by_isbn, add_books_to_user,
    update_book_for_user, delete_book_for_user
)
from utils.logger import get_logger

logger = get_logger(__name__)


@given("I have a valid user and token")
def i_have_a_valid_user_and_token(context):
    context.execute_steps("""
            Given I generate a unique test username and password
            When I send a POST request to create the user
            Then the response status code should be 201
            When I send a POST request to generate a token for the user
            Then the response status code should be 200 and contain a token
        """)


@given("I have a valid user and a book in their collection")
def i_have_a_valid_user_and_a_book_in_their_collection(context):
    context.execute_steps("""
        Given I have a valid user and token
        When I send a POST request to add book with ISBN "9781449325862" to the user's account
        Then the response status code should be 201
    """)


@when("I send a GET request to fetch all books")
def i_send_a_get_request_to_fetch_all_books(context):
    logger.info("Sending GET request to fetch all books")
    context.response = get_all_books(base_url=context.base_url)
    logger.debug(f"Get all books response: {context.response.status_code} - {context.response.text}")


@then("the response should contain a non-empty list of books")
def the_response_should_contain_a_non_empty_list_of_books(context):
    books = context.response.json().get("books", [])
    logger.debug(f"Books received: {books}")
    assert books, f"Expected non-empty list of books. Got: {books}"


@when('I send a GET request to fetch book with ISBN "{isbn}"')
def i_send_a_get_request_to_fetch_book_with_isbn(context, isbn):
    logger.info(f"Fetching book by ISBN: {isbn}")
    context.response = get_book_by_isbn(base_url=context.base_url, isbn=isbn)
    logger.debug(f"Get book response: {context.response.status_code} - {context.response.text}")


@then('the response should contain the book title "{title}"')
def the_response_should_contain_the_book_title(context, title):
    actual_title = context.response.json().get("title")
    logger.debug(f"Expected title: {title}, Actual title: {actual_title}")
    assert actual_title == title, f"Expected title '{title}', got '{actual_title}'"


@when('I send a POST request to add book with ISBN "{isbn}" to the user\'s account')
def i_send_a_post_request_to_add_book_with_isbn_to_the_users_account(context, isbn):
    logger.info(f"Adding book {isbn} to user {context.user_id}")
    context.response = add_books_to_user(base_url=context.base_url,
                                         token=context.token,
                                         user_id=context.user_id,
                                         isbn=isbn)
    logger.debug(f"Add book response: {context.response.status_code} - {context.response.text}")


@when("I send a POST request with ISBN \"{isbn}\" with invalid userId")
def step_impl(context, isbn):
    payload = {
        "userId": "invalid_user_id",
        "collectionOfIsbns": [{"isbn": isbn}]
    }
    context.response = add_books_to_user(base_url=context.base_url,
                                         token=context.token,
                                         user_id=context.user_id,
                                         isbn=isbn,
                                         payload_override=payload)


@when('I send a PUT request to replace book with ISBN "{old_isbn}" with "{new_isbn}"')
def i_send_a_put_request_to_replace_book_with_isbn_with(context, old_isbn, new_isbn):
    logger.info(f"Replacing book {old_isbn} with {new_isbn} for user {context.user_id}")
    context.response = update_book_for_user(base_url=context.base_url,
                                            token=context.token,
                                            user_id=context.user_id,
                                            old_isbn=old_isbn,
                                            new_isbn=new_isbn)
    logger.debug(f"Update book response: {context.response.status_code} - {context.response.text}")


@given('I have a valid user and a book with ISBN "{isbn}" in their collection')
def i_have_a_valid_user_and_a_book_with_isbn_in_their_collection(context, isbn):
    context.execute_steps("""
            Given I generate a unique test username and password
            When I send a POST request to create the user
            Then the response status code should be 201
            When I send a POST request to generate a token for the user
            Then the response status code should be 200 and contain a token
            When I send a POST request to add book with ISBN "9781449325862" to the user's account
            Then the response status code should be 201
        """)


@when('I send a DELETE request to remove book with ISBN "{isbn}"')
def i_send_a_delete_request_to_remove_book_with_isbn(context, isbn):
    logger.info(f"Deleting book {isbn} from user {context.user_id}")
    context.response = delete_book_for_user(base_url=context.base_url,
                                            token=context.token,
                                            user_id=context.user_id,
                                            isbn=isbn)
    logger.debug(f"Delete book response: {context.response.status_code} - {context.response.text}")


@when(u'I send a DELETE request to remove book with ISBN "{isbn}" without user ID')
def step_impl(context, isbn):
    logger.info(f"Deleting book {isbn} from user {context.user_id}")
    payload = {"isbn": isbn}
    context.response = delete_book_for_user(base_url=context.base_url,
                                            token=context.token,
                                            user_id=context.user_id,
                                            isbn=isbn,
                                            payload_override=payload)
    logger.debug(f"Delete book response: {context.response.status_code} - {context.response.text}")


@then('the response status code should be {expected:d}')
def the_response_status_code_should_be(context, expected):
    actual = context.response.status_code
    logger.info(f"Asserting response status code: expected {expected}, actual {actual}")
    logger.debug(f"Full response: {context.response.text}")
    assert actual == expected, f"Expected {expected}, got {actual}. Response: {context.response.text}"
