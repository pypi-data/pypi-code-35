from setupy.features.merge import merge


def test_merge_reproduces_single_dict():
    assert {'a': 1} == merge({'a': 1})


def test_merge_takes_different_keys():
    assert {'a': 1, 'b': 1} == merge({'a': 1}, {'b': 1})


def test_merge_overrides_keys():
    assert {'a': 2} == merge({'a': 1}, {'a': 2})


def test_merge_does_not_work_recursively():
    assert {'a': {'b': {'c': 2}}} == merge({'a': {'b': {'d': 1}}}, {'a': {'b': {'c': 2}}})
