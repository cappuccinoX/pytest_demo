import requests
from utils.log import Logger

class RequestHandler(object):
    def __init__(self):
        self.logger = Logger().get_logger()

    def get(self, url, **kwargs):
        try:
            params = kwargs.get('params')
            headers = kwargs.get('headers')
            rsp = requests.get(url, params = params, headers = headers)
            time_consuming = rsp.elapsed.microseconds/1000
            self.logger.info('请求耗时: %s ms' % (time_consuming))
            return rsp
        except Exception as e:
            self.logger.error('Get 请求 %s 错误: %s' % (url, e))
    
    def post(self, url, **kwargs):
        try:
            params = kwargs.get('params')
            data = kwargs.get('data')
            r_json = kwargs.get('json')
            headers = kwargs.get('headers')
            self.logger.info(f"请求地址: {url}")
            rsp = requests.post(url, params = params, data = data, json = r_json, headers = headers)
            time_consuming = rsp.elapsed.microseconds/1000
            self.logger.info('请求耗时: %s ms' % (time_consuming))
            return rsp
        except Exception as e:
            self.logger.error('Post 请求 %s 错误: %s' % (url, e))

        