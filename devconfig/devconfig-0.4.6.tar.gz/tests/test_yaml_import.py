import pytest
import devconfig
import pythonjsonlogger.jsonlogger
import sys
import logging


def test_import_finder_is_extended(uncached):
    from tests.samples import conf0
    assert conf0.a == 1

def test_logging_configured(uncached):
    devconfig_logger = logging.getLogger('devconfig')
    assert isinstance(devconfig_logger.handlers[0].formatter, pythonjsonlogger.jsonlogger.JsonFormatter)

def test_2_modules_merge_with_extended_module_alredy_cached(uncached):
    from tests.samples import conf0
    from tests.samples import conf1
    assert conf1.b == {'c': {'d': 1, 'e': 4, 'f': 5}}

def test_2_modules_merge_with_extended_module_not_cached(uncached):
    from tests.samples import conf3
    assert conf3.b == {'c': {'d': 1, 'e': 4, 'f': 5}}

def test_module_extends_empty_line(uncached):
    from tests.samples import conf4
    assert conf4.a

def test_module_extends_nonexistent(uncached):
    from tests.samples import conf5
    assert conf5.a