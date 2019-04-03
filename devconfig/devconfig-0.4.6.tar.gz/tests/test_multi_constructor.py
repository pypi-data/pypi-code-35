import pytest
from pprint import pprint
import yaml
import devconfig

def handle_attributes_declared(loader, node, **attributes):
    return attributes

def handle_attributes_undeclared(loader, delimiter, node):
    return delimiter

DECLARED_ATTR_CASES = yaml.load('''
empty_attrs: {}
with_first_attr: { a: a_value }
with_second_attr: { a: null, b: b_value }
with_human_bool_false_a: { a: false }
with_human_bool_true_a: { a: true }
with_human_bool_false_b: { a: no-b, b: false }
with_human_bool_true_b: { a: b, b: true }
with_int_a: { a: 1 }
with_int_b: { a: null, b: 1 }
''')


UNDECLARED_ATTR_CASES = yaml.load('''
empty_without_trailing_colon: ''
empty_with_trailing_colon: ':'
with_attr: ':x'
with_multi_attr: ':x:y'
''')




@pytest.mark.parametrize('case', DECLARED_ATTR_CASES.keys())
def test_multi_constructor_with_declared_attrs(case):
    from tests.samples import multi_constructor
    assert multi_constructor.declared[case] == DECLARED_ATTR_CASES[case]

@pytest.mark.parametrize('case', UNDECLARED_ATTR_CASES.keys())
def test_multi_constructor_with_undeclared_attrs(case):
    from tests.samples import multi_constructor
    assert multi_constructor.undeclared[case] == UNDECLARED_ATTR_CASES[case]