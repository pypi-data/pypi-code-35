# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['preacher',
 'preacher.app',
 'preacher.app.cli',
 'preacher.compilation',
 'preacher.core',
 'preacher.presentation']

package_data = \
{'': ['*']}

install_requires = \
['pyhamcrest>=1.9,<2.0',
 'pyjq>=2.3,<3.0',
 'requests>=2.21,<3.0',
 'ruamel.yaml>=0.15.89,<0.16.0']

entry_points = \
{'console_scripts': ['preacher-cli = preacher.app.cli.main:main']}

setup_kwargs = {
    'name': 'preacher',
    'version': '0.1.0',
    'description': 'A web API verification tool.',
    'long_description': '========\nPreacher\n========\n\n.. image:: https://travis-ci.org/ymoch/preacher.svg?branch=master\n    :target: https://travis-ci.org/ymoch/preacher\n.. image:: https://codecov.io/gh/ymoch/preacher/branch/master/graph/badge.svg\n    :target: https://codecov.io/gh/ymoch/preacher\n.. image:: https://img.shields.io/badge/python-3.7+-blue.svg\n    :target: https://www.python.org/\n\nPreacher verifies API servers,\nwhich requests to API servers and verify the response along to given scenarios.\n\nScenarios are written in `YAML`_ and `jq`_ queries\nso that any developers can write without learning toughly.\n\n\nUsage\n=====\n\nRequirements\n------------\nSupports only Python 3.7+.\n\n.. code-block:: sh\n\n    pip install preacher\n    preacher-cli scenario.yml\n\n    # Help command is available.\n    preacher-cli --help\n\n\nWriting Your Own Scenarios\n==========================\n\nExample\n-------\nHere is a simple configuration example.\n\n.. code-block:: yaml\n\n    scenarios:\n      - label: Simple\n        request:\n          path: /path/to/foo\n        response:\n          status_code: 200\n          body:\n            - describe:\n                jq: .foo\n              it:\n                equals_to: bar\n      - label: A Little Complecated\n        request:\n          path: /path/to/foo\n          params:\n            key1: value\n            key2:\n              - value1\n              - value2\n        response:\n          status_code:\n            - is_greater_than_or_equal_to: 200\n            - is_less_than: 400\n          body:\n            - describe:\n                jq: .foo\n              it:\n                - starts_with: x\n                - ends_wirh: y\n\nGrammer\n-------\n\nGlobal\n******\nA ``Configuration`` is written in `YAML`_.\nA ``Configuration`` is a mapping that consists of below:\n\n- scenarios: ``List<Scenario>``\n    - Scenarios.\n\n\nScenario\n********\nA ``Scenario`` is a mapping that consists of below:\n\n- label: ``String`` (Recommended)\n    - A label of this scenario.\n    - This field is actually optional but recommended to tell a scenario from another.\n- request: ``Request`` (Optional)\n    - A request.\n- response: ``ResponseDescription`` (Optional)\n    - A response description.\n\nRequest\n*******\nA ``Request`` is a mapping that consists of below:\n\n- path: ``String`` (Optional)\n    - A request path. The default value is ``\'\'``.\n- params: ``Mapping<String, String>`` (Optional)\n    - Query parameters as a mapping of keys to values.\n\nResponse Decription\n*******************\nA ``ResponseDescription`` is a mapping that consists of below:\n\n- status_code: ``Integer``, ``Predicate`` or ``List<Predicate>`` (Optional)\n    - Predicates that match a status code as an integer value.\n    - When given a number, that is equivalent to ``{"equals_to": it}``.\n- body: ``Description`` or ``List<Description>`` (Optional)\n    - Descriptions that descript the response body.\n\nDescription\n***********\nA ``Description`` is a mapping that consists of below:\n\n- describe: ``String`` or ``Extraction``\n    - An extraction process.\n    - When given a string, that is passed to the default extraction.\n- it: ``Predicate``, or ``List<Predicate>>``\n    - Predicates that match the extracted value.\n\nExtraction\n**********\nAn ``Extraction`` is a mapping that has one of below:\n\n- jq: ``String``\n    - A `jq`_ query.\n\nPredicate\n*********\nA ``Predicate`` is a string or a mapping. Allowed values are:\n\n- is_null\n- is_not_null\n- is_empty\n- is: ``Value``\n- equals_to: ``Value``\n- has_length: ``Integer``\n- is_greater_than: ``Numeric``\n- is_greater_than_or_equal_to: ``Numeric``\n- is_less_than: ``Numeric``\n- is_less_than_or_equal_to: ``Numeric``\n- contains_string: ``String``\n- starts_with: ``String``\n- ends_with: ``String``\n- matches_regexp: ``String``\n\n\n.. _YAML: https://yaml.org/\n.. _jq: https://stedolan.github.io/jq/\n',
    'author': 'Yu Mochizuki',
    'author_email': 'ymoch.dev@gmail.com',
    'url': 'https://github.com/ymoch/preacher',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
