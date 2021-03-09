'''
提供读取各类测试文件的函数
'''
import json

class ReadData(object):

    root_dir = './test_data/'

    @classmethod
    def read_json(cls, file_name):
        with open(cls.root_dir + file_name) as file:
            data = file.read() 
        return json.loads(data)
    
    @classmethod
    def read_excel(cls, dir):
        return

    @classmethod
    def read_csv(cls, dir):
        return

    @classmethod
    def read_ymal(cls, dir):
        return
