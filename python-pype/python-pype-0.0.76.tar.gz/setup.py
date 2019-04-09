# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['pype', 'pype.plugins']

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
{'console_scripts': ['pype = pype:cli.cli'],
 'pype_plugins': ['basic = pype.plugins']}

setup_kwargs = {
    'name': 'python-pype',
    'version': '0.0.76',
    'description': 'Command-line pipes in Python',
    'long_description': 'pype: command-line pipes in Python\n####################################\n\nUsage\n=====\n\nBasics\n~~~~~~\n\n\nAt the command prompt, use ``pype`` to act on each item in the file with python commands: ::\n\n  $ pype map x.upper() <<<\'abc\'\n  ABC\n\n\nChain python functions together with ``!``: ::\n\n  $ pype map \'x.upper() ! len(x)\' <<<hello\n  5\n\nUse ``x`` as a placeholder for the input at each stage: ::\n\n  $ pype map \' x.split() ! x[0].upper() + "!"\' <<<\'Hello world\'\n  HELLO!\n\n  $ pype map \'x.split() ! x[0].upper() + "!" ! x.replace("H", "J")\' <<<\'Hello world\'\n  JELLO!\n\n\n\nAutomatically import modules you need: ::\n\n   $ pype stack \'itertools.repeat(x, 2) ! "".join\' <<<hello,world!\n   hello,world!\n   hello,world!\n\n\n\nCommands\n~~~~~~~~\n\n``map``\n_______\n\nUse ``map`` to act on each input item. ::\n\n   $ pype map \'x * 2\' <<<\'a\\nbb\\n\'\n   aa\n   bbbb\n\n``filter``\n__________\n\n\nUse ``filter`` to evaluate a condition on each line of input and exclude false values. ::\n\n   $  pype filter \'len(x) > 1\' <<<\'a\\nbb\\nccc\\n\'\n   bb\n   ccc\n\n\n``apply``\n_________\n\nUse ``apply`` to act on the sequence of items. ::\n\n    $   pype apply \'len(x)\' <<<\'a\\nbb\\n\'\n    2\n\n\n``stack``\n_________\n\nUse ``stack`` to treat the input as a single string, including newlines. ::\n\n    $  pype stack \'len(x)\' <<<\'a\\nbb\\n\'\n    5\n\nUse ``eval`` to evaluate a python expression without any input. ::\n\n   $ pype eval 1+1\n   2\n\n``reduce``\n__________\n\nUse ``reduce`` to evaluate a function of two arguments successively over a sequence, like `functools.reduce <https://docs.python.org/3/library/functools.html#functools.reduce>`_ ::\n\n\n   $ pype map int reduce operator.mul <<EOF\n   1\n   2\n   3\n   4\n   EOF\n\n   24\n\n\nAutocall\n~~~~~~~~\n\nYou don\'t need to explicitly call the function with ``f(x)``; just use ``f``. For example, instead of ::\n\n  $ pype map \'len(x)\' <<<\'a\\nbb\'\n  5\n\ntry ::\n\n  $ pype map len <<<\'a\\nbb\'\n  5\n\n\n\nAsync\n~~~~~\n\nMaking sequential requests is slow. These requests take 18 seconds to complete. ::\n\n   $ time pype map \'requests.get ! x.text ! len\' apply max <<EOF\n   http://httpbin.org/delay/5\n   http://httpbin.org/delay/1\n   http://httpbin.org/delay/4\n   http://httpbin.org/delay/3\n   http://httpbin.org/delay/4\n   EOF\n\n   302\n\n   0.61s user\n   0.06s system\n   19.612 total\n\nConcurrent requests can go much faster. The same requests now take only 5 seconds. Just use ``await async_function`` to get concurrency out of the box. ::\n\n   $ time pype map \'await asks.get ! x.text ! len\' apply max <<EOF\n   http://httpbin.org/delay/5\n   http://httpbin.org/delay/1\n   http://httpbin.org/delay/4\n   http://httpbin.org/delay/3\n   http://httpbin.org/delay/4\n   EOF\n\n   297\n\n   0.57s user\n   0.08s system\n   5.897 total\n\n\nStreaming\n~~~~~~~~~\n\n``map`` and ``filter`` values are handled in streaming fashion, while retaining order.\n\nMaking concurrent requests, each response is printed one at a time, as soon as (1) it is ready and (2) all of the preceding requests have already been handled.\n\nFor example, the ``3 seconds`` item is ready before the preceding ``4 seconds`` item, but it is held until the ``4 seconds`` is ready because ``4 seconds`` was started first, so the ordering is maintained.\n\n::\n\n    $ time pype --exec-before \'import datetime; now=datetime.datetime.utcnow; START_TIME=now(); print("Elapsed time | Response size")\' map \'await asks.get !  f"{(now() - START_TIME).seconds} seconds    | {len(x.content)} bytes"\'  <<EOF\n    http://httpbin.org/delay/1\n    http://httpbin.org/delay/2\n    http://httpbin.org/delay/4\n    http://httpbin.org/delay/3\n    EOF\n    Elapsed time | Response size\n    1 seconds    | 297 bytes\n    2 seconds    | 297 bytes\n    4 seconds    | 297 bytes\n    3 seconds    | 297 bytes\n\n\n\nConfiguration\n~~~~~~~~~~~~~\n\nAdd code to automatically execute, into your config file.\n\nFor example: ::\n\n  # ~/.config/pype/config.toml\n\n  exec_before = """\n\n  from itertools import *\n  from collections import Counter\n\n  """\n\nThen you can directly use the imported objects without referencing the module. ::\n\n\n    $ printf \'hello\\nworld\\n\' | pype --autocall map \'Counter ! json.dumps\'\n\n    {"h": 1, "e": 1, "l": 2, "o": 1}\n    {"w": 1, "o": 1, "r": 1, "l": 1, "d": 1}\n\n\nYou can set any of the ``pype`` options in your config. For example, to make ``--no-autocall`` the default, add ::\n\n  # ~/.config/pype/config.toml\n\n  autocall = false\n\nthen just use ``pype`` as normal ::\n\n   $ printf \'a\\nbb\\nccc\\n\' | pype map \'len\'\n   <built-in function len>\n   <built-in function len>\n   <built-in function len>\n\n\nAliases\n~~~~~~~~~~~~~~~~~~\n\nDefine new commands in your config file which provide aliases to other commands. For example, this config adds a ``jsonl`` command for reading jsonlines streams into Python objects, by calling calling out to the ``map`` traversal. ::\n\n\n   [[alias]]\n\n   name = "jsonl"\n   short_help = "Load jsonlines into python objects."\n\n   [[alias.stage]]\n\n   name= "map"\n   options = []\n   arguments = [ "json.loads ! attr.make_class(\'X\', list(x.keys()))(**x)"]\n\n\nNow we can use it like a regular command: ::\n\n    $ pype jsonl  <<< $\'{"a":1, "b":2}\\n{"a": 5, "b":9}\'\n    X(a=1, b=2)\n    X(a=5, b=9)\n\n\nThe new command ``jsonl`` can be used in pipelines as well. To get the maximum value in a sequence of jsonlines objects. ::\n\n   $ pype jsonl map \'x.a\' apply max <<< $\'{"a":1, "b":2}\\n{"a": 5, "b":9}\'\n   5\n\n\nInstallation\n============\n\nGet it with pip: ::\n\n   pip install python-pype\n\n\nCaveats\n=======\n\n\n* ``pype`` assumes *trusted command arguments* and *untrusted input stream data*. It uses ``eval`` on your commands, not on the input stream data. If you use ``exec``, ``eval``, ``subprocess``, or similar commands, you can execute arbitrary code from the input stream, like in regular python.\n\n\nStatus\n======\n\n* Check the `issues page <https://www.github.com/python-pype/pype/issues>`_ for open tickets.\n* This package is experimental pre-alpha and is subject to change.\n\n\nRelated work\n============\n\n* https://github.com/Russell91/pythonpy\n* http://gfxmonk.net/dist/doc/piep/\n* https://spy.readthedocs.io/en/latest/intro.html\n* https://github.com/ksamuel/Pyped\n* https://github.com/ircflagship2/pype\n',
    'author': 'author',
    'author_email': 'author@example.com',
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
