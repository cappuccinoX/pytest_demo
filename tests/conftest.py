import os
import sys
sys.path.append(os.getcwd())
import logging
import pytest
import os,sys
import requests
import json

from requests.models import guess_json_utf

url = "http://localhost:3000"

@pytest.fixture(name="token")
def get_token():
    r = requests.post(
        f"{url}/auth/login",
        data = {"username": "admin", "password": "admin"}
    )
    json_response = json.loads(r.text)
    return json_response["token"]


if __name__ == "__main__":
    print(get_token())
from common.constant import COOKIES
from utils.http import RequestHandler
import re

@pytest.fixture(name="cookies")
def get_cookies():
    return COOKIES

@pytest.fixture(name="company_code")
def company_code():
    request_handler = RequestHandler()
    res = request_handler.get(
        "https://wehr.qq.com/Center/organization/index.html",
        headers = {"Cookie": COOKIES}
    )
    text = res.text
    reg_company_code = r"companyCode\/(.*).html"
    company_code = re.findall(reg_company_code, text)
    return company_code[0]

@pytest.fixture(name = "exam_code")
def exam_code():
    request_handler = RequestHandler()
    res = request_handler.get(
        "https://wehr.qq.com/Center/organization/index.html",
        headers = {"Cookie": COOKIES}
    )
    text = res.text
    reg_exam_code = r"examCode\/(.*)\/bank_id"
    exam_code = re.findall(reg_exam_code, text)
    return exam_code[0]

@pytest.fixture(name = "company_id")
def company_id():
    request_handler = RequestHandler()
    res = request_handler.get(
        "https://wehr.qq.com/Center/organization/index.html",
        headers = {"Cookie": COOKIES}
    )
    text = res.text
    reg_comapany_id = r'id="companyId" value="(.*)"'
    comapany_id = re.findall(reg_comapany_id, text)
    return int(comapany_id[0])


if __name__ == "__main__":
    pass
