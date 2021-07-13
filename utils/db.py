import sys,os
sys.path.append(os.getcwd())
import pymssql
from common.constant import OMS_HOST, OMS_DATABASE, OMS_PASSOWRD, OMS_USER

class SQLServer():
    def __init__(self):
        self.host = OMS_HOST
        self.user = OMS_USER
        self.pwd = OMS_PASSOWRD
        self.db = OMS_DATABASE
    
    def get_connect(self):
        try:
            self.conn = pymssql.connect(
                host=self.host,
                user=self.user,
                password=self.pwd,
                database=self.db,
                charset='utf8'
            )
            cur = self.conn.cursor()
        except Exception as e:
            raise(NameError, f"数据库连接失败: {e}")
        else:
            return cur

    def exec_query(self, sql):
        cur = self.get_connect()
        cur.execute(sql)
        result = cur.fetchall()
        self.conn.close()
        return result

if __name__ == "__main__":
    sql = "select sumqty as '总库存' from u_store_m where wareid ='000434' and busno='0001'"
    s = SQLServer()
    result = s.exec_query(sql)
    print(result)
    print(result[0][0])
    print(type(result[0][0]))
    print(float(result[0][0]))