import os, sys
sys.path.append(os.getcwd())
import pytest
import logging
import requests
import json
from utils.log import Logger
from utils.read_data import ReadData
from utils.http import RequestHandler
from common.constant import DEMO_HOST


@pytest.mark.usefixtures('token')
class Test1:

    def setup_class(self):
        self.logger = Logger().get_logger()
        self.request_handler = RequestHandler()

    @pytest.mark.skip
    @pytest.mark.parametrize('url, limit, expected_code',
        ReadData("list.xlsx").read_excel())
    def test_list_api(self, url, limit, expected_code, token):
        url = f"{DEMO_HOST}{url}"
        rsp = self.request_handler.post(url,  headers={"token": token}, data = {"limit": limit})
        json_data = json.loads(rsp.text)
        assert json_data["code"] == expected_code
    
    @pytest.mark.dependency(name="add")
    def test_add_api(self, token):
        name = "护手霜",
        count = 20
        url = f"{DEMO_HOST}/user/add"
        rsp = self.request_handler.post(
            url,
            headers={"token": token},
            data = {"name": name, "count": count}
        )
        json_data = json.loads(rsp.text)
        assert json_data["code"] == 100

    @pytest.mark.dependency(depends=["add"], scope="module")
    def test_find_api(self, token):
        url = f"{DEMO_HOST}/user/findMedicine"
        rsp = self.request_handler.post(
            url,
            headers={"token": token},
            data = {"id": 1}
        )
        json_data = json.loads(rsp.text)
        assert json_data["code"] == 10
  
    

if __name__ == "__main__":
    pytest.main(["-s", "-v", f"{os.path.abspath('tests')}/test_demo.py"])

    