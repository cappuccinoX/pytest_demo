import os, sys
sys.path.append(os.getcwd())
import pytest
import datetime
import argparse

def parse_param(params):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    testcase = params.testcase
    args = [
        "--capture=tee-sys",
        "-v",
        "%s/%s" % (os.path.abspath("tests"), testcase),
        "--html=%s/%s_report.html" % (os.path.abspath("report"), timestamp)
    ]
    run(args)

def run(args):
    pytest.main(args)


if __name__ == "__main__":
    default_test_case = "%s/test_oms.py" % (os.path.abspath("tests"))
    parser = argparse.ArgumentParser(usage="it's usage tip.", description="help info.")
    parser.add_argument("--testcase", default=default_test_case)
    args = parser.parse_args()
    parse_param(args)