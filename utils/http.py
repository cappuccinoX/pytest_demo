import requests
import logging

class RequestHandler(object):
    def __init__(self):
        pass

    @classmethod
    def get(self, url, **kwargs):
        try:
            params = kwargs.get('params')
            headers = kwargs.get('headers')
            rsp = requests.get(url, params = params, headers = headers)
            time_consuming = rsp.elapsed.microseconds/1000
            logging.info('请求耗时: %s' % (time_consuming))
            return rsp
        except Exception as e:
            logging.error('Get 请求 %s 错误: %s' % (url, e))
    
    def post(self, url, **kwargs):
        try:
            params = kwargs.get('params')
            data = kwargs.get('data')
            r_json = kwargs.get('json')
            headers = kwargs.get('headers')
            rsp = requests.post(url, params = params, data = data, json = r_json, headers = headers)
            time_consuming = rsp.elapsed.microseconds/1000
            logging.info('请求耗时: %s' % (time_consuming))
            return rsp
        except Exception as e:
            logging.error('Post 请求 %s 错误: %s' % (url, e))

        