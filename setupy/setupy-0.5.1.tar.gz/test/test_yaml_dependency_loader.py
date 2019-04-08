from setupy.loaders import YamlDependencyLoader


def test_can_load_feature_from_yaml():
    loader = YamlDependencyLoader()
    feature = loader.load_feature(contents="""name: merge
dependencies:
    imports:
        - from setuptools import setup
        - from setuptools import find_packages
    features:
        - another_feature""", code="""def merge(*dicts):
    r = {}
    for d in dicts:
        r.update(d)
    return r""")

    assert feature.name == "merge"
    assert feature.code == """def merge(*dicts):
    r = {}
    for d in dicts:
        r.update(d)
    return r"""
    assert feature.dependencies("imports") == [
        "from setuptools import setup",
        "from setuptools import find_packages"
    ]
    assert feature.dependencies("features") == [
        "another_feature"
    ]


def test_can_load_setting_from_yaml():
    loader = YamlDependencyLoader()
    setting = loader.load_setting(contents="""name: SETUPY
dependencies:
    imports:
        - from setuptools import find_packages
    features:
        - merge
properties:
    name: "\\"mypackage\\""
    version: "\\"0.1.0\\""
    packages: find_packages(exclude=['contrib', 'docs', 'test'])""")

    assert setting.name == "SETUPY"
    assert setting.properties == {
        "name": "\"mypackage\"",
        "version": "\"0.1.0\"",
        "packages": "find_packages(exclude=['contrib', 'docs', 'test'])"
    }

    assert setting.dependencies("features") == ["merge"]
    assert setting.dependencies("imports") == ["from setuptools import find_packages"]
