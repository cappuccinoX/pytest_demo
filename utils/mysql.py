import pymysql

class MySQL(object):
    def __init__(self):
        self.db = pymysql.connect(
            host = '9.134.192.246',
            port = 3306,
            user = 'mcd',
            passwd = 'mcddev',
            db = 'db_tencent_dna'
        )
        self.cur = self.db.cursor(cursor = pymysql.cursors.DictCursor)
    
    def exec_query(self, query):
        self.cur.execute(query)
        result = self.cur.fetchall()
        return result

    def close(self):
        self.db.close()