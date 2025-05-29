import requests
from behave import given, when, then

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
    url = f"{context.base_url}/Account/v1/User"
    response = requests.post(url, json=context.user_payload, verify=False)
    context.response = response
    if response.status_code == 201:
        context.user_id = response.json().get("userID")


@then("the response status code should be 201")
def step_impl(context):
    assert context.response.status_code == 201, \
        f"Expected 201, got {context.response.status_code}. Response: {context.response.text}"


@when(u'I send a POST request to generate a token for the user')
def step_impl(context):
    url = f"{context.base_url}/Account/v1/GenerateToken"
    response = requests.post(url, json=context.user_payload, verify=False)
    context.response = response
    context.token = response.json().get("token")


@then(u'the response status code should be 200 and contain a token')
def step_impl(context):
    assert context.response.status_code == 200, \
        f"Expected 200, got {context.response.status_code}. Response: {context.response.text}"
    assert context.token, f"Token not found in response: {context.response.json()}"


@then("the user should be retrievable by GET request")
def step_impl(context):
    url = f"{context.base_url}/Account/v1/User/{context.user_id}"
    headers = {
        "Authorization": f"Bearer {context.token}",
        "accept": "application/json"
    }
    response = requests.get(url, headers=headers, verify=False)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.text}"
    data = response.json()
    assert data.get("username") == context.username, \
        f"Expected username '{context.username}', got '{data.get('username')}'"
