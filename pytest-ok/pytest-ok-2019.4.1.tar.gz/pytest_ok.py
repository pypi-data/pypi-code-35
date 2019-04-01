# -*- coding: utf-8 -*-
from __future__ import print_function


def pytest_report_teststatus(report):
    if report.passed and report.when == "teardown":
        print("\nOK")
