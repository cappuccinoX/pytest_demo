import os, sys
sys.path.append(os.getcwd())
import pytest
import json
from utils.log import Logger
from utils.read_data import ReadData
from utils.http import RequestHandler
from utils.assertions import Assertions
from common.constant import DEMO_HOST

@pytest.mark.usefixtures('token')
class Test1:

    def setup_class(self):
        self.logger = Logger().get_logger()
        self.request_handler = RequestHandler()
        self.assertions = Assertions()

    @pytest.mark.skip
    @pytest.mark.parametrize('url, limit, expected_code',
        ReadData("list.xlsx").read_excel())
    def test_list_api(self, url, limit, expected_code, token):
        url = f"{DEMO_HOST}{url}"
        rsp = self.request_handler.post(url,  headers={"token": token}, data = {"limit": limit})
        json_data = json.loads(rsp.text)
        self.assertions.assert_code(expected_code, json_data["code"])
    
    @pytest.mark.skip
    @pytest.mark.dependency()
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
        self.assertions.assert_code(10, json_data["code"])

    @pytest.mark.skip
    @pytest.mark.dependency(depends=["Test1::test_add_api"], scope="class")
    def test_find_api(self, token):
        url = f"{DEMO_HOST}/user/findMedicine"
        id = 1
        rsp = self.request_handler.post(
            url,
            headers={"token": token},
            data = {"id": id}
        )
        json_data = json.loads(rsp.text)
        self.assertions.assert_code(10, json_data["code"])
        self.assertions.assert_value(json_data, id, "id")
    
if __name__ == "__main__":
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    pytest.main([
        "-s",
        "-v",
        f"--html={os.path.abspath('report')}/{timestamp}_report.html",
        f"{os.path.abspath('tests')}/test_demo.py"
    ])

    