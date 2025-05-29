from datetime import datetime


def get_current_timestamp():
    """
    Returns the current timestamp in the format YYYYMMDDHHMMSS
    :return: str
    """
    return datetime.now().strftime("%Y%m%d%H%M%S")
