# -*- coding: utf-8 -*-

import csv
import tempfile
import threading

import psutil
import pytest


def pytest_addoption(parser):
    group = parser.getgroup('memprof')
    group.addoption(
        '--memprof-top-n',
        action='store',
        dest='memprof_top_n',
        default=0,
        help='limit memory reports to top n entries, report all if value is 0',
    )

    group.addoption(
        '--memprof-csv-file',
        action='store',
        dest='memprof_csv_file',
        default=None,
        help='output comma separated value table to given filename',
    )

    parser.addini('memprof_top_n', 'limit memory reports to top n entries')
    parser.addini('memprof_csv_file', 'output comma separated value table to given filename')


mem_consumptions = {}


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item):

    avail = lambda: psutil.virtual_memory().available

    before = avail()

    peaks = []
    running = [True]

    def report_mem():
        peaks.append(avail())
        if running:
            # run this function in 0.3 seconds again:
            threading.Timer(0.3, report_mem).start()

    report_mem()

    yield

    # stop running:
    running[:] = []

    key = "::".join(item.listnames()[1:])

    after = min(peaks + [avail()])
    increase = before - after
    if increase > 0:
        mem_consumptions[key] = increase


def fmt_mem(mem):
    kb, b = divmod(mem, 1024)
    mb, kb = divmod(kb, 1024)
    if mb:
        return "%.1f MB" % (mem / 1024.0 / 1024.0)
    if kb:
        return "%.1f KB" % (mem / 1024.0)
    else:
        return "%.2f B" % mem


@pytest.hookimpl(hookwrapper=True)
def pytest_terminal_summary(terminalreporter, exitstatus):

    tr = terminalreporter

    top_n = tr.config.option.memprof_top_n
    csv_filename = tr.config.option.memprof_csv_file

    try:
        top_n = int(top_n)
    except ValueError:
        raise ValueError("given parameter --memprof-top-n is no int")

    items = sorted(mem_consumptions.items(), key=lambda item: -item[1])

    if top_n:
        items = items[:top_n]

    if items:
        tr.section("memory consumption estimates")
        numc = max([len(name) for name, value in items]) + 1
        filler = numc * " "
        for name, value in items:
            tr.write((name + filler)[:numc] + " - ")
            tr.write(fmt_mem(value) + "\n", bold=True)

        if csv_filename:
            with open(csv_filename, 'wt') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['function', 'memory'])
                writer.writerows(items)
    yield

