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

class TestOMS():

    def setup_class(self):
        self.logger = Logger().get_logger()
        self.request_handler = RequestHandler()
        self.assertions = Assertions()
        self.sql_server = SQLServer()        

    '''
    id: 商品编码
    chailing: 是否拆零:1不拆零，2拆零
    good_count: 零售商品数量
    inventory_diff: 库存差预期值
    remark: 备注：商品拆零系数
    expected_code: 零售接口返回字段code预期值
    '''
    @pytest.mark.parametrize(
        "url, id, chailing, good_count, expected_inventory_diff, remark, expected_code",
        ReadData("lingshou.xlsx").read_excel()
    )
    def test_lingshou(self, url, id, chailing, good_count, expected_inventory_diff, remark, expected_code):
        order_no = str(random.randint(555555, 9999999999))
        self.logger.info(f"随机生成订单号: {order_no}")
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
            "orderNo": order_no,
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
            "isBatchNoStock": 0,
            "healthNum":0,
            "healthValue":0,
            "ware": [
                    {
                    "erpCode": id,
                    "goodsName": "永孜堂小黄订单测试商品【000175】ha 0.4克*12片*3板",
                    "goodsType": 1,
                    "batchNo": "222222",
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
            "adjustno": None
        }

        # 调取零售接口
        rsp = self.request_handler.post(
            url,
            json = lingshou_data,
        )
        json_body = json.loads(rsp.text)
        assert json_body["code"] == expected_code
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
