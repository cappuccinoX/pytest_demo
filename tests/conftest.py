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

# 临时文件
@pytest.fixture(name="tmp_file", scope="class")
def oms_tmp_file(tmpdir_factory):
    fn = tmpdir_factory.mktemp("tmp").join("tmp.txt")
    return fn


if __name__ == "__main__":
    print(get_token())