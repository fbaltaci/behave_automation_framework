import requests

from utils.logger import get_logger

logger = get_logger(__name__)

# --- API Endpoints ---
ACCOUNT_USER_ENDPOINT = "/Account/v1/User"
ACCOUNT_GENERATE_TOKEN_ENDPOINT = "/Account/v1/GenerateToken"
BOOKSTORE_BOOKS_ENDPOINT = "/BookStore/v1/Books"
BOOKSTORE_BOOK_ENDPOINT = "/BookStore/v1/Book"


def create_user(base_url, payload, custom_path=None, custom_headers=None):
    """
    Creates a new user with the provided payload.

    :param base_url: Base URL of the API
    :param payload: Payload containing user details
    :param custom_path: Custom path to override the default endpoint
    :param custom_headers: Custom headers to override the default headers
    :return: Response object
    """
    path = custom_path or ACCOUNT_USER_ENDPOINT
    url = f"{base_url}{path}"
    headers = custom_headers or {"Content-Type": "application/json", "accept": "application/json"}

    logger.info(f"Creating user with username: {payload['userName']}")
    response = requests.post(url=url, headers=headers, json=payload, verify=False)
    logger.debug(f"User creation response: {response.status_code} - {response.text}")

    return response


def generate_token(base_url, payload, custom_path=None, custom_headers=None):
    """
    Generates a token for the user with the provided payload.
    :param base_url: Base URL of the API
    :param payload: Payload containing username and password
    :param custom_path: Custom path to override the default endpoint
    :param custom_headers: Custom headers to override the default headers
    :return: Response object
    """
    path = custom_path or ACCOUNT_GENERATE_TOKEN_ENDPOINT
    url = f"{base_url}{path}"
    headers = custom_headers or {"Content-Type": "application/json", "accept": "application/json"}

    response = requests.post(url=url, headers=headers, json=payload, verify=False)
    logger.debug(f"Token generation response: {response.status_code} - {response.text}")

    return response


def retrieve_user(base_url, user_id, token, custom_path=None, custom_headers=None):
    """
    Retrieves user details for the given user ID.
    :param base_url: Base URL of the API
    :param user_id: User ID to retrieve
    :param token: Authorization token
    :param custom_path: Custom path to override the default endpoint
    :param custom_headers: Custom headers to override the default headers
    :return: Response object
    """
    path = custom_path or ACCOUNT_USER_ENDPOINT
    url = f"{base_url}{path}/{user_id}"
    headers = custom_headers or {"accept": "application/json", "Authorization": f"Bearer {token}"}

    logger.info(f"Fetching user with ID: {user_id}")
    response = requests.get(url=url, headers=headers, verify=False)
    logger.debug(f"Retrieve user response: {response.status_code} - {response.text}")

    return response


def get_all_books(base_url, custom_path=None, custom_headers=None):
    """
    Fetches all books from the bookstore.
    :param base_url: Base URL of the API
    :param custom_path: Custom path to override the default endpoint
    :param custom_headers: Custom headers to override the default headers
    :return: Response object
    """
    path = custom_path or BOOKSTORE_BOOKS_ENDPOINT
    url = f"{base_url}{path}"
    headers = custom_headers or {"accept": "application/json"}

    logger.info("Sending GET request to fetch all books")
    response = requests.get(url=url, headers=headers, verify=False)
    logger.debug(f"Get all books response: {response.status_code} - {response.text}")

    return response


def get_book_by_isbn(base_url, isbn, custom_path=None, custom_headers=None):
    """
    Fetches a book by its ISBN.
    :param base_url: Base URL of the API
    :param isbn: ISBN of the book to fetch
    :param custom_path: Custom path to override the default endpoint
    :param custom_headers: Custom headers to override the default headers
    :return: Response object
    """
    path = custom_path or BOOKSTORE_BOOK_ENDPOINT
    url = f"{base_url}{path}?ISBN={isbn}"
    headers = custom_headers or {"accept": "application/json"}

    logger.info(f"Fetching book by ISBN: {isbn}")
    response = requests.get(url=url, headers=headers, verify=False)
    logger.debug(f"Get book response: {response.status_code} - {response.text}")

    return response


def add_books_to_user(base_url, token, user_id, isbn, custom_path=None, custom_headers=None, payload_override=None):
    """
    Adds a book to the user's collection.
    :param base_url: Base URL of the API
    :param token: Authorization token
    :param user_id: User ID to add the book to
    :param isbn: ISBN of the book to add
    :param custom_path: Custom path to override the default endpoint
    :param custom_headers: Custom headers to override the default headers
    :param payload_override: Custom payload to override the default payload
    :return: Response object
    """
    path = custom_path or BOOKSTORE_BOOKS_ENDPOINT
    url = f"{base_url}{path}"
    headers = custom_headers or {
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
    }
    payload = payload_override or {"userId": user_id, "collectionOfIsbns": [{"isbn": isbn}]}

    logger.info(f"Adding book {isbn} to user {user_id}")
    response = requests.post(url=url, json=payload, headers=headers, verify=False)
    logger.debug(f"Add book response: {response.status_code} - {response.text}")

    return response


def update_book_for_user(base_url, token, user_id, old_isbn, new_isbn, custom_path=None, custom_headers=None,
                         payload_override=None):
    """
    Replaces a book in the user's collection with another book.
    :param base_url: Base URL of the API
    :param token: Authorization token
    :param user_id: User ID to update the book for
    :param old_isbn: ISBN of the book to replace
    :param new_isbn: ISBN of the new book
    :param custom_path: Custom path to override the default endpoint
    :param custom_headers: Custom headers to override the default headers
    :param payload_override: Custom payload to override the default payload
    :return: Response object
    """
    path = custom_path or BOOKSTORE_BOOKS_ENDPOINT
    url = f"{base_url}{path}"
    headers = custom_headers or {
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
    }
    payload = payload_override or {"userId": user_id, "isbn": new_isbn}

    logger.info(f"Replacing book {old_isbn} with {new_isbn} for user {user_id}")
    response = requests.put(url=url, json=payload, headers=headers)
    logger.debug(f"Update book response: {response.status_code} - {response.text}")

    return response


def delete_book_for_user(base_url, token, user_id, isbn, custom_path=None, custom_headers=None, payload_override=None):
    """
    Deletes a book from the user's collection.
    :param base_url: Base URL of the API
    :param token: Authorization token
    :param user_id: User ID to delete the book from
    :param isbn: ISBN of the book to delete
    :param custom_path: Custom path to override the default endpoint
    :param custom_headers: Custom headers to override the default headers
    :param payload_override: Custom payload to override the default payload
    :return: Response object
    """
    path = custom_path or BOOKSTORE_BOOK_ENDPOINT
    url = f"{base_url}{path}"
    headers = custom_headers or {
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
    }
    payload = payload_override or {"userId": user_id, "isbn": isbn}

    logger.info(f"Deleting book {isbn} from user {user_id}")
    response = requests.delete(url=url, json=payload, headers=headers, verify=False)
    logger.debug(f"Delete book response: {response.status_code} - {response.text}")

    return response
