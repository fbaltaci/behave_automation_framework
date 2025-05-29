import requests


def create_user(base_url, payload):
    url = f"{base_url}/Account/v1/User"
    return requests.post(url, json=payload, verify=False)


def generate_token(base_url, payload):
    url = f"{base_url}/Account/v1/GenerateToken"
    return requests.post(url, json=payload, verify=False)


def retrieve_user(base_url, user_id, token):
    url = f"{base_url}/Account/v1/User/{user_id}"
    headers = {
        "Authorization": f"Bearer {token}",
        "accept": "application/json"
    }
    return requests.get(url, headers=headers, verify=False)
