from behave import given, when, then
import requests


@given('I have new user credentials "{username}" and "{password}"')
def step_impl(context, username, password):
    context.new_user_payload = {
        "userName": username,
        "password": password
    }


@when("I send a POST request to create the user")
def step_impl(context):
    url = f"{context.base_url}/Account/v1/User"
    response = requests.post(url, json=context.new_user_payload, verify=False)
    context.response = response


@then("the response status code should be 201 or 406")
def step_impl(context):
    assert context.response.status_code in [201, 406], \
        f"Expected 201 or 406, got {context.response.status_code}. Response: {context.response.text}"
