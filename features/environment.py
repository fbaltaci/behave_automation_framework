import os
from dotenv import load_dotenv
import urllib3

load_dotenv()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def before_all(context):
    context.base_url = os.getenv("BASE_URL")
