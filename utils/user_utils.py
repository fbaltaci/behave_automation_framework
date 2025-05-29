from utils.date_utils import get_current_timestamp

def generate_unique_credentials():
    """
    Generates a unique username using the current timestamp.
    Returns a tuple: (username, password)
    """
    timestamp = get_current_timestamp()
    username = f"testuser_{timestamp}"
    password = "StrongPass123!"
    return username, password
