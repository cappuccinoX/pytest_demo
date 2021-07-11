import pytest
import logging
import requests
import json
# from utils.http import HttpRequest

log = logging.getLogger(__name__)
scode = 'b94029246782fbfe4f9d29a1e23a152305844dbf'
mcduid = 170603

@pytest.mark.usefixtures('token')
class Test1:
    @pytest.mark.skip
    @pytest.mark.parametrize('user, pwd',
        [
            ('jack', 12345),
            ('Andy', 2223)
        ])
    # @pytest.mark.skip
    def test_3(self, user, pwd):
        log.info('User is {user}, password is {pwd}'.format(user = user, pwd = pwd))
    
    # @pytest.mark.skip
    def test_demo_token(self, token):
        log.info(token)

if __name__ == "__main__":
    import os
    pytest.main(["-s", "-v", f"{os.path.abspath('tests')}/test_demo.py"])

    