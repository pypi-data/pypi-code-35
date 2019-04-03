import pytest
from importlib import import_module
from inspect import isclass
import devconfig

class shortform_with_testattr:
    testattr = True

class shortform_without_testattr:
    pass

class longform_with_failing_classattr:
    testattr = False

class longform_with_correct_classattr:
    testattr = True

@pytest.mark.parametrize('class_attr', (
                                        'shortform_with_classattr',
                                        'shortform_with_bases',
                                        'longform_with_classattr',
                                        'longform_with_bases',
                                        ))
def test_class_mixer(uncached, class_attr):
    # each constructed class must be instance of type
    # each constructed class must contain attr `testattr` == True
    _class = getattr(import_module('tests.samples.class_mixer'), class_attr)
    assert isclass(_class)
    assert hasattr(_class, 'testattr')
    assert _class.testattr == True


