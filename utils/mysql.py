import sys, os
sys.path.append(os.getcwd())
import pymysql

class MySQL(object):
    def __init__(self, host, port, user, passwd, db):
        self.db = pymysql.connect(
            host = host,
            user = user,
            passwd = passwd,
            db = db
        )
        self.cur = self.db.cursor(cursor = pymysql.cursors.DictCursor)
    
    def exec_query(self, query):
        try:
            self.cur.execute(query)
            result = self.cur.fetchall()
            return result
        finally:
            self.db.close()

if __name__ == "__main__":
    sql = MySQL("10.200.25.32", 3306, "hydee", "hydee@soft123", "hydee")
    result = sql.exec_query("select id,inter_type,order_amt,await_flag from u_interface_sale_indent_m where platformno='0001';")
    print(result)