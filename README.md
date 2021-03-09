pytest-rerunfailures 失败后重新执行插件
pytest-html 测试报告插件
pytest-xdist 并行运行插件
pytest-sugar 运行时可以显示进度条

并行执行
pytest -n 数字

本地插件打包发布
包根目录下配置setup.py文件
eg：
from setuptools import setup
setup(
    name="xx"
    version="xxx"
    description="xx"
    url="xx"
    author="xx"

)
python3 setup.py sdist
pip3 install dist/xxxx.tar.gz

pytest-dependency 解决依赖执行的插件
eg: @pytest.mark.dependency(depends=["类名::函数名", "类名::函数名"]) 
或者直接写入函数名

运行命令举例
pytest .\tests\test_db.py --html=test_db_report.html --capture=sys