'''
封装断言方法
'''

import json
from utils.log import Logger

class Assertions(object):
    def __init__(self):
        self.logger = Logger().get_logger()

    def assert_code(self, expected_code, code):
        '''
        校验response code
        '''
        try:
            assert expected_code == code
            return True
        except Exception as e:
            self.logger.error('Error happened in assert_code func, meet error: %s' % e)
            raise

    def assert_body(self, body, expected_key):
        '''
        校验response是否包含指定字段
        '''
        try:
            keys = body.keys()
            assert expected_key in keys
        except Exception as e:
            self.logger.error('Error happened in assert_body func, meet error: %s' % e)
            raise

    def assert_value(self, body, expected_value, key):
        '''
        校验response指定字段的值是否正确
        '''
        try:
            actual_value = body[key]
            assert actual_value == expected_value
        except Exception as e:
            self.logger.error('Error happened in assert_text func, meet error: %s' % e)
            raise