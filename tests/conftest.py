import os
import sys
sys.path.append(os.getcwd())
import logging
import pytest
import os,sys
import requests
import json
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