'''
提供读取各类测试文件的函数
'''
import json, csv, xlrd, os, datetime
from xlrd import xldate_as_tuple
from utils.log import Logger

class ReadData(object):

    root_dir = os.path.abspath("test_data")

    def __init__(self, file_name):
        self.file_path = f"{self.root_dir}/{file_name}"
        self.logger = Logger().get_logger()

    def read_json(self, file_name):
        try:
            with open(self.file_path + file_name) as file:
                json_data = json.loads(file.read())
            return json_data
        except Exception as e:
            self.logger.error(f"读取json文件错误: {e}")
    
    def read_excel(self):
        try:
            data = list()
            book = xlrd.open_workbook(self.file_path)
            sheet = book.sheet_by_index(0)
            rows = sheet.nrows
            cols = sheet.ncols
            # 第一行是标题, 从第二行读取
            for r in range(1, rows):
                row_data = list()
                for c in range(cols):
                    ctype = sheet.cell(r, c).ctype # 表格的数据类型
                    cell = sheet.cell_value(r, c)
                    if ctype == 2 and cell % 1 == 0: # 整型
                        cell = int(cell)
                    elif ctype == 3:
                        # 转成datetime对象
                        date = datetime(*xldate_as_tuple(cell, 0))
                        cell = date.strftime('%Y/%d/%m %H:%M:%S')
                    elif ctype == 4:
                        cell = True if cell == 1 else False
                    row_data.append(cell)
                data.append(row_data)
            self.logger.info(data)
            return data
        except Exception as e:
            self.logger.error(f"读取excel错误: {e}")

    def read_csv(self):
        try:
            data = list()
            with open(self.file_path, "r") as file:
                reader = csv.reader(file)
                # 忽略第一行title
                next(reader)
                for item in reader:
                    data.append(item)
                return data
        except Exception as e:
            self.logger.error(f"读取csv错误: {e}")

    def read_ymal(self):
        return

if __name__ == "__main__":
    r = ReadData("test_demo.xlsx")
    r.read_excel()
