"""pytest options that can be used as test fixtures"""

from collections import namedtuple
from pathlib import Path
import json
from typing import List
import pytest


Option = namedtuple("Option", (
    "type",
    "name",
    "help",
    "default",
    "scope"))

OPTION_DEFAULTS = (str, None, None, None, "module")
Option.__new__.__defaults__ = OPTION_DEFAULTS  # type: ignore


ConfigOption = namedtuple("ConfigOption", (
    "name",
    "help",
    "default",
    "searchpath"))


def _register_as_config_fixture(
        option: ConfigOption,
        globals_,
        parser):

    fixture_option_ = Option(
        type=str,
        name=option.name,
        help=option.help,
        scope="session",
        default=None
    )

    def make_config_file_reader(request):
        file_name = request.config.getoption("--" + option.name)
        abs_file_name = Path(option.searchpath) / file_name

        def get_from_configfile_(option_name):
            return _fetch_config_option(abs_file_name, option_name)

        return get_from_configfile_

    return _register_as_fixture_function(
        option=fixture_option_,
        fixture_function=make_config_file_reader,
        globals_=globals_,
        parser=parser)


def _raise(*args, **kwargs):
    raise RuntimeError()


def _register_as_fixture_function(
        option: Option,
        fixture_function,
        globals_,
        parser):
    fixture_function.__name__ = option.name.replace("-", "_")
    fixture_function.__doc__ = option.help
    fixture = pytest.fixture(scope=option.scope)(fixture_function)
    assert option.name not in globals_
    globals_[option.name] = fixture
    parser.addoption(
        "--" + option.name,
        action="store",
        help=option.help,
        type=option.type,
    )
    return fixture_function


def _register_as_fixture(option: Option, globals_, parser, fallback):
    def fixture_function(request):
        value = _maybe(request.config.getoption("--" + option.name))
        return value or fallback(request)(option.name)
    return _register_as_fixture_function(
        option=option,
        globals_=globals_,
        parser=parser,
        fixture_function=fixture_function)


def _fetch_config_option(config_file: Path, option_name: str):
    config = json.load(config_file.open())
    return config[option_name]


def _maybe(arg: str):
    return None if arg == "None" else arg


def register(
        globals_,
        parser,
        options: List[Option]):
    """add options to pytest that can be used as test fixtures"""
    for opt in options:
        _register_as_fixture(opt, globals_, parser, fallback=_raise)


def register_with_config_fallback(
        globals_,
        parser,
        configfile_option: ConfigOption,
        other_options: List[Option]):
    """add options to pytest that can be used as test fixtures"""
    config_reader = _register_as_config_fixture(
        option=configfile_option,
        globals_=globals_,
        parser=parser)
    for opt in other_options:
        _register_as_fixture(opt, globals_, parser, fallback=config_reader)
