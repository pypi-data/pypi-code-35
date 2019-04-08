from setupy.core.model import Setup
from setupy.core.setting import Setting
from setupy.core.serialize import serialize_imports, serialize_settings, serialize_features
from test.mocks import MockDependencyLoader


def test_serializer_can_serialize_with_imports():
    setup = Setup(MockDependencyLoader())
    setup.add_import("from setuptools import setup")
    setup.add_import("from setuptools import find_packages")
    setup.add_import("from os import path")
    setup.add_import("from io import open")

    assert serialize_imports(setup) == """from io import open
from os import path

from setuptools import find_packages, setup
"""


def test_serializer_can_serialize_features():
    mdl = MockDependencyLoader()
    mdl.a_feature("test", code="""def merge(*dicts):
    r = {}
    for d in dicts:
        r.update(d)
    return r""")

    mdl.a_feature("test2", code="""def merge(*dicts):
    r = {}
    for d in dicts:
        r.update(d)
    return r""")

    setup = Setup(mdl)
    setup.add_feature("test")
    setup.add_feature("test2")

    assert serialize_features(setup) == """def merge(*dicts):
    r = {}
    for d in dicts:
        r.update(d)
    return r

def merge(*dicts):
    r = {}
    for d in dicts:
        r.update(d)
    return r"""


def test_serializer_can_serialize_settings():
    mdl = MockDependencyLoader()
    mdl.a_setting('BASE', properties={
        "name": "\"setupy\"",
        "version": "\"0.1.0\"",
        "packages": "find_packages(exclude=['contrib', 'docs', 'test'])"
    })

    setup = Setup(mdl)
    setup.add_setting('BASE')

    serialized_settings, _ = serialize_settings(setup)

    assert serialized_settings == """BASE = {
    "name": "setupy",
    "version": "0.1.0",
    "packages": find_packages(exclude=['contrib', 'docs', 'test'])
}"""


def test_serializer_can_deserialize_nested_dictionary_setting():
    mdl = MockDependencyLoader()
    mdl.a_setting('BASE', properties={
        "name": "\"setupy\"",
        "version": "\"0.1.0\"",
        "packages": "find_packages(exclude=['contrib', 'docs', 'test'])",
        "extra_requires": {
            "dev": ["\"pytest\""]
        }
    })

    setup = Setup(mdl)
    setup.add_setting('BASE')

    serialized_settings, _ = serialize_settings(setup)

    assert serialized_settings == """BASE = {
    "name": "setupy",
    "version": "0.1.0",
    "packages": find_packages(exclude=['contrib', 'docs', 'test']),
    "extra_requires": {
        "dev": ["pytest"]
    }
}"""
