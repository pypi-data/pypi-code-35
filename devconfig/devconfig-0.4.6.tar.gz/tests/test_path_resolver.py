import pytest
from pathlib import Path
from functools import partial
import yaml
import devconfig
from pprint import pprint
from unittest.mock import _Call

UNIT_CASES = """
empty:
    yaml: |
        --- !tag:devconfig:extend/resolver/path:
        {}
        ---
        {}
    result: []
root_single_kinded:
    yaml: |
        --- !tag:devconfig:extend/resolver/path:
        .!construct: mapping
        ---
        {}
    result: 
    - - !!python/tuple
        - '!construct'
        - !!python/tuple []
      - {kind: !!python/name:builtins.dict ''}
root_single_kinded_with_fallback:
    yaml: |
        --- !tag:devconfig:extend/resolver/path:
        .!construct: mapping
        .!defaultroot:
        ---
        {}
    result: 
    - - !!python/tuple
        - '!construct'
        - !!python/tuple []
      - {kind: !!python/name:builtins.dict ''}
    - - !!python/tuple
        - '!defaultroot'
        - !!python/tuple []
      - {kind: null}
root_multi_kinded_with_fallback:
    yaml: |
        --- !tag:devconfig:extend/resolver/path:
        .!construct1: mapping
        .!construct2: sequence
        .!construct3: scalar
        .!defaultroot:
        ---
        {}
    result: 
    - - !!python/tuple
        - '!construct1'
        - !!python/tuple []
      - {kind: !!python/name:builtins.dict ''}
    - - !!python/tuple
        - '!construct2'
        - !!python/tuple []
      - {kind: !!python/name:builtins.list ''}
    - - !!python/tuple
        - '!construct3'
        - !!python/tuple []
      - {kind: !!python/name:builtins.str ''}
    - - !!python/tuple
        - '!defaultroot'
        - !!python/tuple []
      - {kind: null}

nested_explicit_key_single_kinded:
    yaml: |
        --- !tag:devconfig:extend/resolver/path:
        mapping:
            subkey:
                .!construct-subkey-mapping: mapping
        ---
        subkey: #!construct-subkey-mapping
            x: 1
            y: 2
    result:
    - - !!python/tuple
        - '!construct-subkey-mapping'
        - !!python/tuple
          - !!python/tuple [&id001 !!python/name:builtins.dict '', subkey]
      - {kind: *id001}

nested_implicit_key_single_kinded:
    yaml: |
        --- !tag:devconfig:extend/resolver/path:
        mapping:
            null:
                .!construct-subkey-mapping: mapping
        ---
        subkey0: #!construct-subkey-mapping
            x: 1
            y: 2
        subkey1: # not matched - kind is list
            - 1
            - 2
    result:
    - - !!python/tuple
        - '!construct-subkey-mapping'
        - !!python/tuple
          - !!python/tuple [&id002 !!python/name:builtins.dict '', null]
      - {kind: *id002}

nested_explicit_key_multi_kinded:
    yaml: |
        --- !tag:devconfig:extend/resolver/path:
        mapping:
            null:
                .!construct-subkey-mapping: mapping
                .!construct-subkey-sequence: sequence
        ---
        subkey0: #!construct-subkey-mapping
            x: 1
            y: 2
        subkey1: #!construct-subkey-sequence
            - 1
            - 2
    result:
    - - !!python/tuple
        - '!construct-subkey-mapping'
        - !!python/tuple
          - &id004 !!python/tuple [&id003 !!python/name:builtins.dict '', null]
      - {kind: *id003}
    - - !!python/tuple
        - '!construct-subkey-sequence'
        - !!python/tuple
          - *id004
      - {kind: !!python/name:builtins.list ''}


nested_implicit_key_single_kinded_with_nested_index_constructors_with_fallback:
    yaml: |
        --- !tag:devconfig:extend/resolver/path:
        .!rootconstructor:
        mapping:
            null:
                .!construct-subkey-mapping: mapping
                sequence:
                    0:
                        .!construct-subkey-mapping-nested-list-mapping: mapping
                    false:
                        .!construct-subkey-mapping-nested-sublist: sequence
        --- #whole object constructed with !rootconstructor
        subkey0: #!construct-subkey-mapping
            - {a: 1} #!construct-subkey-mapping-nested-list-mapping
            #!construct-subkey-mapping-nested-sublist
            - - 1 
              - 2
            - {c: 2} # not matched
            #!construct-subkey-mapping-nested-sublist
            - - 3 
              - 4
        subkey1: #!construct-subkey-mapping
            #!construct-subkey-mapping-nested-sublist
            - - 0
            #!construct-subkey-mapping-nested-sublist
            - - 1
              - 2
        subkey3: #!construct-subkey-mapping
            a: 1  # not matched
            b: 2  # not matched

    result:
    - - !!python/tuple
        - '!rootconstructor'
        - !!python/tuple []
      - {kind: null}
    - - !!python/tuple
        - '!construct-subkey-mapping'
        - !!python/tuple
          - &id006 !!python/tuple [&id005 !!python/name:builtins.dict '', null]
      - {kind: *id005}
    - - !!python/tuple
        - '!construct-subkey-mapping-nested-list-mapping'
        - !!python/tuple
          - *id006
          - !!python/tuple [&id007 !!python/name:builtins.list '', 0]
      - {kind: *id005}
    - - !!python/tuple
        - '!construct-subkey-mapping-nested-sublist'
        - !!python/tuple
          - *id006
          - !!python/tuple [*id007, false]
      - {kind: *id007}

"""


UNIT = yaml.load(UNIT_CASES)


@pytest.mark.parametrize('case', UNIT.keys())
def test_path_resolver(loader, mocked_add_path_resolver, case):
    case = UNIT[case]
    initial_extensions = len(loader.extensions)
    for document in devconfig.documents(case['yaml']):
        doc = document.loader.construct_document(document)
    # print('parsed yaml:')
    # print(case['yaml'])
    # print('added path resolver:')
    # print(yaml.dump([list(callresult) for callresult in mocked_add_path_resolver.call_args_list]))
    assert mocked_add_path_resolver.call_args_list == case['result']

