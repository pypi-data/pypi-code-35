from setupy.setupy import setupy
from test.mocks import MockDependencyLoader


def test_can_produce_its_own_config():
    mdl = MockDependencyLoader()
    mdl.a_feature("merge", code="""def merge(*dicts):
    r = {}
    for d in dicts:
        r.update(d)
    return r""")

    mdl.a_setting("BASE", features=["merge"], imports=[
        "from setuptools import find_packages",
        "from setuptools import setup"
    ], properties={
        "name": "\"mypackage\"",
        "version": "\"0.1.0\"",
        "packages": "find_packages(exclude=['contrib', 'docs', 'test'])"
    })

    mdl.a_setting("SETUPY", properties={
        "name": "\"setupy\"",
        "version": "\"0.1.0\"",
    })

    assert setupy(settings=["BASE", "SETUPY"], dependency_loader=MockDependencyLoader()) == """from setuptools import find_packages, setup


def merge(*dicts):
    r = {}
    for d in dicts:
        r.update(d)
    return r

BASE = {
    "name": "mypackage",
    "version": "0.1.0",
    "packages": find_packages(exclude=['contrib', 'docs', 'test'])
}

SETUPY = {
    "name": "setupy",
    "version": "0.1.0"
}



setup(**merge(BASE, SETUPY))"""
