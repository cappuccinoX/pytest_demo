import pytest
import logging
import requests
import json
# from utils.http import HttpRequest

log = logging.getLogger(__name__)
scode = 'b94029246782fbfe4f9d29a1e23a152305844dbf'
mcduid = 170603

# @pytest.mark.usefixtures('connectDb')
class Test1:
    @pytest.mark.parametrize('user, pwd',
        [
            ('jack', 12345),
            ('Andy', 2223)
        ])
    @pytest.mark.skip
    def test_3(self, user, pwd):
        log.info('User is {user}, password is {pwd}'.format(user = user, pwd = pwd))

    @pytest.mark.skip
    def test_4(self):
        # rsp = HttpRequest.get('http://httpbin.org/json')
        rsp = requests.get(
            'https://wehr.qq.com/Center/company/historyadminlist',
            cookies = {
                'mcduid': '170603',
                'scode': 'b94029246782fbfe4f9d29a1e23a152305844dbf'
            },
        )
        log.info(rsp.json())
    
    @pytest.mark.skip
    def test_5(self):
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36'}
        rsp = requests.post(
            'https://at-bos-api-develop.atfxdev.com/v1/privilege/user_list',
            cookies = {
                'authentication': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2NvdW50IjoiYWRtaW4iLCJpYXQiOjE2MTQzMjc2MDksImV4cCI6MTYxNDQxNDAwOX0.DJOpRrUvuEaSg-VfGn13Wm5jA_WMZlSifd_X8HwgFqc'
            },
            headers = headers,
            data = {"sortBy":"createDate","sort":"desc","page":1,"limit":999999,"searchKey":"userName","searchVal":""}
        )
        log.info(rsp)

def test_f1(username, f1):
    log.info(username)
    log.info(f1)