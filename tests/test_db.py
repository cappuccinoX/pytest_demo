import py
import pytest
import logging
import pymysql
import json
from utils.mysql import MySQL
from utils.file import ReadData
from utils.log import Log

@pytest.mark.usefixtures('tips')
def test_db(tips):
    mysql = MySQL()
    data = mysql.exec_query("SELECT * FROM `exam` where code in ('4A65EFEB94F5C11B81ED');")
    Log.info(json.dumps(data))
    mysql.close()

ids = [
    '姓名: {}, 年龄: {}, 性别: {}'.
        format(data['name'], data['age'], data['sex']) for data in ReadData.read_json('profile.json')
]

@pytest.mark.parametrize('name, age, sex', ReadData.read_json('profile.json'), ids = ids)
def test_01(name, age, sex):
    Log.info('Name is {name}, age is {age}, sex is {sex}'.format(name = name, age = age, sex = sex))