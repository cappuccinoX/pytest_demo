import pymysql

class MySQL(object):
    def __init__(self):
        self.db = pymysql.connect(
            host = '127.0.0.1',
            port = 3306,
            user = 'root',
            passwd = '12345678',
            db = 'jpress'
        )
        self.cur = self.db.cursor(cursor = pymysql.cursors.DictCursor)
    
    def exec_query(self, query):
        try:
            self.cur.execute(query)
            result = self.cur.fetchall()
            return result
        finally:
            self.db.close()