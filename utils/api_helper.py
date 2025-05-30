import requests

from utils.logger import get_logger

logger = get_logger(__name__)


def create_user(base_url, payload):
    url = f"{base_url}/Account/v1/User"

    logger.info(f"Creating user with username: {payload['userName']}")
    response = requests.post(url, json=payload, verify=False)
    logger.debug(f"User creation response: {response.status_code} - {response.text}")

    return response


def generate_token(base_url, payload):
    url = f"{base_url}/Account/v1/GenerateToken"

    logger.info(f"Generating token for user: {payload['userName']}")
    response = requests.post(url, json=payload, verify=False)
    logger.debug(f"Token generation response: {response.status_code} - {response.text}")

    return response


def retrieve_user(base_url, user_id, token):
    url = f"{base_url}/Account/v1/User/{user_id}"
    headers = {
        "Authorization": f"Bearer {token}",
        "accept": "application/json"
    }

    logger.info(f"Fetching user with ID: {user_id}")
    response = requests.get(url, headers=headers, verify=False)
    logger.debug(f"Retrieve user response: {response.status_code} - {response.text}")

    return response


def get_all_books(base_url):
    url = f"{base_url}/BookStore/v1/Books"
    headers = {"accept": "application/json"}

    logger.info("Sending GET request to fetch all books")
    response = requests.get(url, headers=headers, verify=False)
    logger.debug(f"Get all books response: {response.status_code} - {response.text}")

    return response


def get_book_by_isbn(base_url, isbn):
    url = f"{base_url}/BookStore/v1/Book?ISBN={isbn}"
    headers = {"accept": "application/json"}

    logger.info(f"Fetching book by ISBN: {isbn}")
    response = requests.get(url, headers=headers, verify=False)
    logger.debug(f"Get book response: {response.status_code} - {response.text}")

    return response


def add_books_to_user(base_url, token, user_id, isbn):
    url = f"{base_url}/BookStore/v1/Books"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
    }
    payload = {
        "userId": user_id,
        "collectionOfIsbns": [{"isbn": isbn}]
    }

    logger.info(f"Adding book {isbn} to user {user_id}")
    response = requests.post(url, json=payload, headers=headers, verify=False)
    logger.debug(f"Add book response: {response.status_code} - {response.text}")

    return response


def update_book_for_user(base_url, token, user_id, old_isbn, new_isbn):
    url = f"{base_url}/BookStore/v1/Books/{old_isbn}"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
    }
    payload = {
        "userId": user_id,
        "isbn": new_isbn
    }
    logger.info(f"Replacing book {old_isbn} with {new_isbn} for user {user_id}")
    response = requests.put(url, json=payload, headers=headers)
    logger.debug(f"Update book response: {response.status_code} - {response.text}")

    return response


def delete_book_for_user(base_url, token, user_id, isbn):
    url = f"{base_url}/BookStore/v1/Book"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
    }
    payload = {
        "userId": user_id,
        "isbn": isbn
    }

    logger.info(f"Deleting book {isbn} from user {user_id}")
    response = requests.delete(url, json=payload, headers=headers, verify=False)
    logger.debug(f"Delete book response: {response.status_code} - {response.text}")

    return response
