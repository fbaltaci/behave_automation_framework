import os

import allure
import allure_behave
import urllib3
from dotenv import load_dotenv

load_dotenv()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def before_all(context):
    context.allure_adapter = allure_behave.AllureReporter()
    context.base_url = os.getenv("BASE_URL")


def after_step(context, step):
    if step.status == "failed":
        allure.attach(
            body=context.response.text if hasattr(context, 'response') else "No response",
            name="Failure Response",
            attachment_type=allure.attachment_type.TEXT,
        )
