'''
调试文件
'''
import pytest, os, sys

@pytest.mark.parametrize('passwd',
                      ['123456'])
class Test():
    @pytest.mark.dependency(name="1")
    def test_1(self, passwd):
        assert 1==1

    @pytest.mark.dependency(name="2", depends=["1"], scope="class")
    def test_2(self, passwd):
        assert 1==2

    @pytest.mark.dependency(depends=["1","2"], scope="class")
    def test_3(self, passwd):
        assert 1==1


if __name__ == "__main__":
    pytest.main([
        "-s",
        "-v",
        f"{os.path.abspath('tests')}/test_demo1.py"
    ])
    