一、使用介绍
1. 安装python，安装后在命令行输入python --version 检查是否安装成功
2. 命令行执行 pip install -r requirements.txt 安装项目依赖包
3. 按照以下命令运行用例
   a. 命令行运行 pytest -s -v tests/test_oms.py
   b. 如果需要查看运行报告，命令行运行 pytest -s -v --html=./report/report.html tests/test_oms.py

二、项目目录介绍
1. common 存放常量
2. Log 记录代码运行日志
3. report 存放报告
4. test_data 存放测试数据
5. tests 存放测试用例
6. utils 存放工具函数
7. pytest.ini 配置文件
8. conftest.py 固件管理文件以及自定义测试报告