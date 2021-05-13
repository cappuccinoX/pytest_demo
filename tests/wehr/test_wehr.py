from utils.http import RequestHandler
import pytest
import json
from common.wehr_api import update_questionnaire_type, exam_type

@pytest.mark.usefixtures("cookies")
@pytest.mark.usefixtures("company_code")
@pytest.mark.usefixtures("exam_code")
@pytest.mark.usefixtures("company_id")
class Test_wehr():

    def setup_class(self):
        self.req_handler = RequestHandler()

    # 完善公司信息
    def test_complete_company_info(self, cookies, company_code, exam_code):
        res = self.req_handler.post(
            "https://wehr.qq.com/Home/Organ/companyDraft",
            headers = {
                "Cookie": cookies
            },
            data = {
                "companyCode":company_code,
                "examCode":exam_code,
                "grow_speed":3,
                "profit_ability":2,
                "creative_ability":3,
                "market_share":3,
                "branding_img":3,
                "year_establish":2005,
                "companies_involved":1,
                "development_phase":1,
                "sales_revenue":3,
                "interest_rate":2,
                "manage_num":40,
                "employee_num":500,
                "flag":1            
            }
        )
        assert res.text == "1", "完善公司信息失败"

    '''
    自定义问卷
    '''
    def test_custom_exam(self, cookies, exam_code, company_id):
        pass
        # 选择问卷类型
        # self.questionnaire_type(2, cookies, exam_code)
        # 选择调研形式
        # self.exam_type(2, cookies, exam_code, company_id)
    '''
    选择问卷类型
    type = 1 组织能力调研 type = 2 组织能力+敬业度
    '''
    def test_questionnaire_type(self, cookies, exam_code):
        res = self.req_handler.post(
            update_questionnaire_type,
            headers = {"Cookie": cookies},
            data = {"examCode": exam_code, "type": 1}
        )
        res = res.json()
        assert res["status"] == 1, "选择问卷类型失败"

    '''
    选择调研形式
    type = 1 一人一码 type = 2 普通调研
    '''
    def test_exam_type(self, cookies, exam_code, company_id):
        res = self.req_handler.post(
            exam_type,
            headers = {"Cookie": cookies},
            data = {"examCode": exam_code, "type": 2, "companyId": company_id}
        )
        res = res.json()
        assert res["status"] == 1, "选择问卷类型失败"

    @pytest.mark.parametrize()
    def test_save_grade(self, cookies, exam_code):
        res = self.req_handler.post(
            exam_type,
            headers = {"Cookie": cookies},
            data = {"exam_code": exam_code, "bank_id": 2, "data": ""}
        )
        res = res.json()
        assert res["status"] == 1, "选择问卷类型失败"
