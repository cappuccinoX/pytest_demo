import os, sys
sys.path.append(os.getcwd())
import json
from utils.log import Logger
from utils.read_data import ReadData
from utils.http import RequestHandler
from utils.assertions import Assertions
import pytest
from utils.db import SQLServer
import random

'''
id: 商品编码
chailing: 是否拆零:1不拆零，2拆零
good_count: 零售商品数量
inventory_diff: 库存差预期值
remark: 备注：商品拆零系数
lingshou_exp_code: 零售接口返回字段code预期值
jiedan_exp_code: 接单接口返回字段code预期值
jianhuo_exp_code: 拣货接口返回字段code预期值
'''
@pytest.mark.parametrize(
    "id, chailing, good_count, expected_inventory_diff, remark, lingshou_exp_code, jiedan_exp_code, jianhuo_exp_code",
    ReadData("lingshou.xlsx").read_excel()
)
@pytest.mark.usefixtures("tmp_file")
class TestOMS():
    
    def setup_class(self):
        self.logger = Logger().get_logger()
        self.request_handler = RequestHandler()
        self.assertions = Assertions()
        self.sql_server = SQLServer()
        self.order_no = str(random.randint(555555, 9999999999))     
        self.logger.info(f"随机生成订单号: {self.order_no}")

    # @pytest.mark.skip
    @pytest.mark.dependency(name="jiedan")
    def test_jiedan(self, id, chailing, good_count, expected_inventory_diff, remark, lingshou_exp_code, jiedan_exp_code, jianhuo_exp_code, tmp_file):
        url = "http://hudit-r-h1.test.ydjia.cn/o2o_jiedan"
        jiedan_data = {
            "busno": "0001",
            "flag": 1,
            "merCode": "888888",
            "orderno": self.order_no,
            "sign": "IeZvG7iUhqunXI1QJZ38miw868t+T/wMSuoAkck+/HdrfA/BQvVjh7TZUOxGSMyTxYyCvxeWYFOF51Yz5/wC6J5ZPixNND4nsNIzST5Zsl3GCDD4Q5wDC805JHDoR0cZ6L04L0t17XycqVJhw8YPvwcfj9k/zx8wPgJbsLW4Du1wBOp34sp8aTu2LgCjhJj1StyCcR57VOrOpnVlTifZ880/kUOlFky+yUttadnC87rv/Ub0C78Au90/Df3aT0sRXb7XeYPzga04vIGPeCcwJzBjH0qWw6QpZYiZeVCUF3AzzNv01NUwUTW2K04lwWQOquePoQCt3Uk0sNjUEfRtaA==",
            "signTimestamp": 1609902814271,
            "signType": "RSA2",
            "userID": 2012,
            "ware": [
                        {
                    "warecode": id,
                    "wareqty": good_count,
                    "goodsType":1,
                    "chailing": chailing
                }        
            ],
        }
        rsp = self.request_handler.post(
            url,
            json = jiedan_data
        )
        json_body = json.loads(rsp.text)
        assert json_body["code"] == jiedan_exp_code
        adjust_no = json_body["data"]["adjustno"] # 单号
        makeno = json_body["data"]["make"][0]["makeno"] # 批号
        data = {"adjust_no": adjust_no, "makeno": makeno}
        tmp_file.write(json.dumps(data))
        self.logger.info(f"接单单号: {adjust_no}, 批号: {makeno}")

    # @pytest.mark.skip
    @pytest.mark.dependency(name="jianhuo", depends=["jiedan"])
    def test_jianhuo(self, id, chailing, good_count, expected_inventory_diff, remark, lingshou_exp_code, jiedan_exp_code, jianhuo_exp_code, tmp_file):
        data = tmp_file.read()
        data = json.loads(data)
        url = "http://hudit-r-h1.test.ydjia.cn/o2o_jianhuo"
        jianhuo_data = {
            "merCode": "888888",
            "signType": "RSA2",
            "signTimestamp": 1609333735636,
            "sign": "EMmZbIlQ0Ircy+OBlakYiJUuSOe3pMHL1Huyba1zz/F5peB3FUiTkn8WOSbZK37ZBMZ/Ym+iD9908s3r9qBJPRYc2O+BRRWfdS36Gs8xYk0z3qFYokgLphd3ZcZRX3cO5YEqhJGz+JSUze5RYonOh3Hf98dhHtX3OaJGDiEKxYLjyLqsdS4to6V0ITQtZlYI4E8jO5gl2Aa1zwlbaJxzXAMA58oTcyImOyQL/hYulf1iaqcC17y2wqOA3IHf3PeEKZr72JRuSjjlD8PkJSqYAr/fmMo3kI6npIpceIMOlusssEDTlLpp9UE5weEGt1t4uPgnqDHw9WnxUjWcOyjuKw==",
            "flag": 1,
            "ware": [
                {
                    "goodsType": 1,
                    "warecode": id,
                    "wareqty": good_count,
                    "makeno": data["makeno"],
                    "chailing": chailing
                }
            ],
            "userID": 168,
            "orderno": self.order_no,
            "busno": "0001",
            "adjustno": data["adjust_no"]
        }
        rsp = self.request_handler.post(
            url,
            json = jianhuo_data
        )
        json_body = json.loads(rsp.text)
        assert json_body["code"] == jianhuo_exp_code

    # @pytest.mark.skip
    @pytest.mark.dependency(depends=["jiedan", "jianhuo"])
    def test_lingshou(self, id, chailing, good_count, expected_inventory_diff, remark, lingshou_exp_code, jiedan_exp_code, jianhuo_exp_code, tmp_file):
        data = tmp_file.read()
        data = json.loads(data)
        url = "http://hudit-r-h1.test.ydjia.cn/o2o_lingshou_v2"
        # 零售前查询库存
        sql_shouqian = f"select sumqty as '总库存' from u_store_m where wareid = '{id}' and busno='0001'"
        shouqian = self.sql_server.exec_query(sql_shouqian)

        if len(shouqian) == 0:
            self.logger.error(f"根据条件wareid = '{id}' and busno='0001'查询u_store_m表没有数据")
            assert False
        val1 = float(shouqian[0][0])
        lingshou_data = {
            "mercode": "888888",
            "signType": "RSA2",
            "signTimestamp": 1609903095815,
            "sign": "nYeSqG2HJH/cnXUYkzXp5P6o9PnuAsG9VDZV//ruJezy9d1aIRXuMlU2qtciMs+77hfdc03ZG/Se3h7LwgTCV2X4jkE1ZQNsmABMbYXmbz0qclrwJiGpXv76CuTRpC3PE+tip1MyyD2mRIBsj3SROzSWvf08Jn0aq2p5tLomzpfOUDijkp5fw19A1RK2Oh5fjBbTZ1uKV2XEFVj3ip/fvsVm8/0yFB/R6wiwLnV4Aq5O6L9xyvWyjiWoMEidbiJ5Z5o5lML/R2UrFvjyCZfrnk842eyXTC2SZIHohyLY0l1TMKP/Ox+1Pi54nocpsBz5ADeAKwo3b5/4ZyPeDAYQTA==",
            "orderNo": self.order_no,
            "orderType": 0,
            "prescriptionFlag": 0,
            "deliveryTimeType": 0,
            "deliveryTypeName": "0",
            "orderState": 30,
            "thirdOrderNo": "1688105423358051073",
            "thirdPlatCode": "43",
            "thirdPlatName": "微商城",
            "organizationCode": "0001",
            "buyerName": "小黄测试",
            "receiverName": "小黄测试",
            "reveiverAddress": "湖南省长沙市岳麓区湖南省长沙市岳麓区麓天路19号附近7楼",
            "receiverPhone": "13142123253",
            "buyerActualAmount": 10.1,
            "merchantActualReceive": 36.11,
            "goodsTotalAmount": 10.1,
            "deliveryFee": 0.00,
            "platformDeliveryFee": 0.00,
            "packageFee": 0.00,
            "platformPackFee": 0.00,
            "totalAmount": 11.11,
            "merchantDiscount": 0.00,
            "platformDiscount": 0.00,
            "brokerageAmount": 0.00,
            "buyerRemark": "测试123456",
            "created": 1609902802000,
            "dayNum": "7",
            "acceptTime": 1609902813000,
            "memberNo": "20200421000001",
            "userId": "1010 ",
            "deliveryUserId": "1010 ",
            "payCode": "809081",
            "cashierSource": "",
            "discountAmount": 0.00,
            "dutyId": "",
            "isBatchNoStock": 1, # 是否按批号下账；1按指定批号; 0不指定按批号
            "healthNum":0,
            "healthValue":0,
            "ware": [
                    {
                    "erpCode": id,
                    "goodsName": "永孜堂小黄订单测试商品【000175】ha 0.4克*12片*3板",
                    "goodsType": 1,
                    "batchNo": data["makeno"],
                    "goodsCount": good_count,
                    "price": 10.1,
                    "goodsAmount": 11.11,
                    "shareAmount": 0.00,
                    "billAmount": 11.11,
                    "billPrice": 36.11,
                    "status": 0,
                    "chailing": chailing
                },
            ],
                "payTypeList": [
                {
                "payCode": "809080",
                "payName": "OMS线上支付",
                "payPrice": 11.11
                },
                {
                "payCode": "809081",
                "payName": "OMS线下支付",
                "payPrice": 25.00
                }
            ],
            "paytype": "线上支付",
            "adjustno": data["adjust_no"]
        }
        # 调取零售接口
        rsp = self.request_handler.post(
            url,
            json = lingshou_data,
        )
        json_body = json.loads(rsp.text)
        assert json_body["code"] == lingshou_exp_code
        # 零售后查询库存
        sql_shouhou = f"select sumqty as '总库存' from u_store_m where wareid = '{id}' and busno='0001'"
        shouhou = self.sql_server.exec_query(sql_shouhou)

        if len(shouhou) == 0:
            self.logger.error(f"根据条件wareid = '{id}' and busno='0001'查询u_store_m表没有数据")
            assert False

        val2 = float(shouhou[0][0])
        assert val2 - val1 == expected_inventory_diff



if __name__ == "__main__":
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    pytest.main([
        "-s",
        "-v",
        f"--html={os.path.abspath('report')}/{timestamp}_report.html",
        f"{os.path.abspath('tests')}/test_oms.py"
    ])
