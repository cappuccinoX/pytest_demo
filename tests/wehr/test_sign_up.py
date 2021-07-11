import pytest
import json
from utils.http import RequestHandler

@pytest.mark.usefixtures("cookies")
class Test_Signup():

    def setup_class(self):
        self.req_handler = RequestHandler()

    # 组织能力报名
    def test_sign_up(self, cookies):
        res = self.req_handler.post(
            "https://wehr.qq.com/Home/Organ/apply/step/1.html",
            headers = {"Cookie": cookies},
            data = {
                "step": 2,
                "name": "michael_脚本生成公司",
                "simple": "脚本生成公司",
                "businessType": 103,
                "contactName": 123,
                "contactDegree": 123,
                "contactPhone": 123,
                "contactEmail": "123@qqq.com"
            }
        )
        assert res.status_code == 200, "组织能力报名失败"

if __name__ == "__main__":
    pytest.main(["-s", "-v", "test_sign_uo.py"])