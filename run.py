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
        "--html=%s/%s_report.html" % (os.path.abspath("report"), timestamp)
    ]
    if testcase != None:
        testcase = "%s/%s" % (os.path.abspath("tests"), testcase)
        args.append(testcase)
    run(args)

def run(args):
    pytest.main(args)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage="it's usage tip.", description="help info.")
    parser.add_argument("--testcase")
    args = parser.parse_args()
    parse_param(args)