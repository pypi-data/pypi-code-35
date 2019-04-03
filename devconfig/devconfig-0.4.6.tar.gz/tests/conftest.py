import pytest
import yaml
import yaml.resolver
from importlib import invalidate_caches


tested_loggers = ['devconfig',]

@pytest.yield_fixture
def mocked_iterload(mocker):
    _load = yaml.load
    yaml.load = mocker.Mock()
    yield yaml.load 
    yaml.load = _load


@pytest.yield_fixture
def empty_yaml_open_file():
    with open('tests/samples/empty.yaml', 'r') as empty_yaml:
        yield empty_yaml


@pytest.yield_fixture(scope='function')
def uncached():
    invalidate_caches()
    yield None


@pytest.yield_fixture(scope='function')
def loader():
    try:
        yield devconfig.context.push()
    finally:
        devconfig.context.pop()

@pytest.yield_fixture(scope='function')
def mocked_add_path_resolver(mocker):
    _add_path_resolver = yaml.Loader.add_path_resolver
    yaml.Loader.add_path_resolver = mocker.Mock()
    yield yaml.Loader.add_path_resolver
    yaml.Loader.add_path_resolver = _add_path_resolver

import devconfig