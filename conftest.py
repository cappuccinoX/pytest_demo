'''
固件管理文件, 后期可根据实际需求在各目录新建专属的固件管理文件conftest.py
'''
import pytest
from py._xmlgen import html

# 自定义命令行运行参数
def pytest_addoption(parser):
    parser.addoption('--username', action = 'store', help = '')

# 获取自定义的命令行参数
@pytest.fixture()
def username(request):
    return request.config.getoption('--username')

def pytest_configure(config):
    config._metadata['项目名称'] = 'pytest_demo'
    config._metadata.pop('JAVA_HOME')

@pytest.mark.optionalhook
def pytest_html_results_summary(prefix):
    prefix.extend([html.p('测试人员: Michael')])

@pytest.mark.optionalhook
def pytest_html_results_table_header(cells):
    cells.pop(-1) # 删除results列表倒数第一列Links

@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    cells.pop(-1) # 删除results列表倒数第一列Links

# 定义报告title
def pytest_html_report_title(report):
    report.title = "My demo test report"