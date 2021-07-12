import os, sys
sys.path.append(os.getcwd())
import pytest
import pymysql
import json
from utils.mysql import MySQL
from common.constant import DEMO_HOST, DB_HOST, DB_PORT, USER, PASSWORD, DB
class TestDB():
    
    def setup_class(self):
        db = MySQL(DB_HOST, DB_PORT, USER, PASSWORD, DB)
        self.cur = db.cursor(cursor = pymysql.cursors.DictCursor)

    
    def test_db(self):
        self.cur.execute("SELECT * FROM test_demo.medicine_info;")
        result = self.cur.fetchall()
        print(result)

if __name__ == "__main__":
    pytest.main([
        "-s",
        "-v",
        f"{os.path.abspath('tests')}/test_db.py"
    ])
