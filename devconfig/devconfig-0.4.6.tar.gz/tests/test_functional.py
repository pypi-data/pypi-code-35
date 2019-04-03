import pytest
from pathlib import Path
from functools import partial
import yaml
import devconfig
from pprint import pprint

RESOLVER_CASES = """
nested_and_merged_and_referred:
    yaml: |
        --- !tag:devconfig:extend/resolver/path:testsubresolver
        .!attributed:tests.samples.path_resolver_constructor.DummyObject: mapping
        --- !tag:devconfig:extend/resolver/path:
        ~dummy: &dummy !resolver:testsubresolver
        mapping:
            null:
              <<: *dummy
              .!attributed:tests.samples.path_resolver_constructor.DefaultDummyObject:
              mapping:
                value:
                  mapping:
                    subkey: *dummy
        ---
        subkey0:
          value: 1234
        subkey1:
          value:
            a: 1
        subkey2:
          - this is value
        subkey3: false
        subkey4:
          - false
        subkey5:
          value: false
        subkey6:
          value:
            subkey:
              value:
                call_this_example_with: python3 -c 'import devconfig; from tests.samples import path_resolver; import pprint; pprint.pprint(vars(path_resolver))'

    result:
    - subkey0: !!python/object:tests.samples.path_resolver_constructor.DummyObject {value: 1234}
      subkey1: !!python/object:tests.samples.path_resolver_constructor.DummyObject
        value: {a: 1}
      subkey2: !!python/object:tests.samples.path_resolver_constructor.DefaultDummyObject {
        value: this is value}
      subkey3: false
      subkey4: !!python/object:tests.samples.path_resolver_constructor.DefaultDummyObject {
        value: false}
      subkey5: !!python/object:tests.samples.path_resolver_constructor.DummyObject {value: false}
      subkey6: !!python/object:tests.samples.path_resolver_constructor.DummyObject
        value:
          subkey: !!python/object:tests.samples.path_resolver_constructor.DummyObject
            value: {call_this_example_with: python3 -c 'import devconfig; from tests.samples
                import path_resolver; import pprint; pprint.pprint(vars(path_resolver))'}

"""

RESOLVER = yaml.load(RESOLVER_CASES)

@pytest.mark.parametrize('case', RESOLVER.keys())
def test_path_resolver(loader, case):
    case = RESOLVER[case]
    result = []
    for document in devconfig.documents(case['yaml']):
        result.append(document.loader.construct_document(document))
    # print('parsed yaml:')
    # print(case['yaml'])
    # print('result:')
    # print(yaml.dump(result))
    assert result == case['result']

FSTRING_CASES = """
rendered_fstring:
    yaml: |
        --- &lobals
        gggg: &globals
          number: 1
          x: 1
          y: !path zzzz
          z: zzzz
          k: !$:globals "{type(x)}-{type(y)}-{type(z)}-y:{y}"
          pathtype: !!python/name:pathlib.Path
          e: !envvar:AX
            default: 1

        testf: !$:globals "we-got-number-{number}-{type(z)}"
        kkk: !$:lobals "{gggg['pathtype']}"
        # c: !f:lobals "{d}-{abs(_local)}-{c}"
        d: 221

    result:
    - d: 221
      gggg:
        e: 1
        k: <class 'int'>-<class 'str'>-<class 'str'>-y:zzzz
        number: 1
        pathtype: !!python/name:pathlib.Path ''
        x: 1
        y: !!python/object/apply:pathlib.PosixPath [zzzz]
        z: zzzz
      kkk: <class 'pathlib.Path'>
      testf: we-got-number-1-<class 'str'>


"""

FSTRING = yaml.load(FSTRING_CASES)

@pytest.mark.parametrize('case', FSTRING.keys())
def test_fstring(loader, case):
    case = FSTRING[case]
    result = []
    for document in devconfig.documents(case['yaml']):
        result.append(document.loader.construct_document(document))
    # print('parsed yaml:')
    # print(case['yaml'])
    # print('result:')
    # print(yaml.dump(result))
    assert result == case['result']