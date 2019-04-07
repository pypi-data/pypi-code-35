# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pype']

package_data = \
{'': ['*']}

install_requires = \
['appdirs',
 'async_exit_stack',
 'async_generator',
 'attrs',
 'bump2version',
 'click',
 'click-default-group',
 'parso',
 'toml',
 'toolz',
 'trio']

entry_points = \
{'console_scripts': ['pype = pype:cli.cli']}

setup_kwargs = {
    'name': 'python-pype',
    'version': '0.0.63',
    'description': 'Command-line pipes in Python',
    'long_description': 'pype: command-line pipes in Python\n####################################\n\nUsage\n=====\n\nBasics\n~~~~~~\n\n\nAt the command prompt, use ``pype`` to act on each item in the file with python commands: ::\n\n  $ printf \'abc\' | pype map x.upper()\n\n  ABC\n\n\nChain python functions together with ``!``: ::\n\n  $ printf \'Hello\'  | pype map \'x.upper() ! len(x)\'\n\n  5\n\nUse ``x`` as a placeholder for the input at each stage: ::\n\n  $ printf \'Hello World\'  | pype map \' x.split() ! x[0].upper() + "!"\'\n\n  HELLO!\n\n  $ printf \'Hello World\'  | pype map \'x.split() ! x[0].upper() + "!" ! x.replace("H", "J")\'\n\n  JELLO!\n\n\n\n\n\nGiven a server responding to ``http://localhost:8080/`` and a list of urls in ``urls.txt`` : ::\n\n  http://localhost:8080/Requester_254\n  http://localhost:8080/Requester_083\n  http://localhost:8080/Requester_128\n  http://localhost:8080/Requester_064\n  http://localhost:8080/Requester_276\n\n\nAutomatically import required modules and use their functions: ::\n\n   $ pype map \'x.strip() ! requests.get(x) ! x.text \' < urls.txt\n\n   Hello, Requester_254. You are client number 7903 for this server.\n   Hello, Requester_083. You are client number 7904 for this server.\n   Hello, Requester_128. You are client number 7905 for this server.\n   Hello, Requester_064. You are client number 7906 for this server.\n   Hello, Requester_276. You are client number 7907 for this server.\n\n\nCommands\n~~~~~~~~\n\n``map``\n_______\n\n  Use ``map`` to act on each input item. ::\n\n\n   $  printf \'a\\nbb\\n\' | pype map \'x * 2\'\n   aa\n   bbbb\n\n``filter``\n__________\n\n\nUse ``filter`` to evaluate a condition on each line of input and exclude false values. ::\n\n   $ printf \'a\\nbb\\nccc\\n\' | pype filter \'len(x) > 1\'\n   bb\n   ccc\n\n\n``apply``\n_________\n\nUse ``apply`` to act on the sequence of items. ::\n\n    $ printf \'a\\nbb\\n\' | pype apply \'len(x)\'\n    2\n\n\n``stack``\n_________\n\nUse ``stack`` to treat the input as a single string, including newlines. ::\n\n    $ printf \'a\\nbb\\n\' | pype stack \'len(x)\'\n    5\n\nUse ``eval`` to evaluate a python expression without any input. ::\n\n   $ pype eval 1+1\n   2\n\nOptions\n~~~~~~~\n\n``--autocall``\n______________\n\nIf you\'re tired of writing all those ``f(x)``, use ``--autocall``, and just write ``f`` without the ``(x)``. ::\n\n    $ printf \'hello\\neverybody\\n\' | pype --autocall map \'len\'\n    5\n    9\n\n\nAsync\n~~~~~\n\nMaking sequential requests is slow. These requests take 10 seconds to complete. ::\n\n  $ time pype map \'str.strip ! requests.get ! x.text\'  < urls.txt\n\n  Hello, Requester_254. You are client number 8061 for this server.\n  Hello, Requester_083. You are client number 8062 for this server.\n  Hello, Requester_128. You are client number 8063 for this server.\n  Hello, Requester_064. You are client number 8064 for this server.\n  Hello, Requester_276. You are client number 8065 for this server.\n\n  real\t0m10.640s\n  user\t0m0.548s\n  sys\t0m0.022s\n\n\nMaking concurrent requests is much faster: ::\n\n   $ time pype map \'x.strip() ! await asks.get(x) ! x.text\'  < urls.txt\n\n   Hello, Requester_254. You are client number 8025 for this server.\n   Hello, Requester_083. You are client number 8025 for this server.\n   Hello, Requester_128. You are client number 8025 for this server.\n   Hello, Requester_064. You are client number 8025 for this server.\n   Hello, Requester_276. You are client number 8025 for this server.\n\n   real\t0m2.626s\n   user\t0m0.574s\n   sys\t0m0.044s\n\n\nConfiguration\n~~~~~~~~~~~~~\n\nAdd code to automatically execute, into your config file.\n\nFor example: ::\n\n  # ~/.config/pype/config.toml\n\n  exec_before = """\n\n  from itertools import *\n  from collections import Counter\n\n  """\n\nThen you can directly use the imported objects without referencing the module. ::\n\n\n    $ printf \'hello\\nworld\\n\' | pype --autocall map \'Counter ! json.dumps\'\n\n    {"h": 1, "e": 1, "l": 2, "o": 1}\n    {"w": 1, "o": 1, "r": 1, "l": 1, "d": 1}\n\n\nYou can set any of the ``pype`` options in your config. For example, to make ``--no-autocall`` the default, add ::\n\n  # ~/.config/pype/config.toml\n\n  autocall = false\n\nthen just use ``pype`` as normal ::\n\n   $ printf \'a\\nbb\\nccc\\n\' | pype map \'len\'\n   <built-in function len>\n   <built-in function len>\n   <built-in function len>\n\n\nInstallation\n============\n\nGet it with pip: ::\n\n   pip install python-pype\n\n\nCaveats\n=======\n\n\n* ``pype`` assumes *trusted command arguments* and *untrusted input stream data*. It uses ``eval`` on your commands, not on the input stream data. If you use ``exec``, ``eval``, ``subprocess``, or similar commands, you can execute arbitrary code from the input stream, like in regular python.\n\n\nStatus\n======\n\n* Check the `issues page <https://www.github.com/python-pype/pype/issues>`_ for open tickets.\n* This package is experimental pre-alpha and is subject to change.\n\n\nRelated work\n============\n\n* https://github.com/Russell91/pythonpy\n* http://gfxmonk.net/dist/doc/piep/\n* https://spy.readthedocs.io/en/latest/intro.html\n* https://github.com/ksamuel/Pyped\n* https://github.com/ircflagship2/pype\n',
    'author': 'author',
    'author_email': 'author@example.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
