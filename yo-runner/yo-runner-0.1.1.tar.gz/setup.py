# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['yo']
install_requires = \
['pyyaml>=3.13']

entry_points = \
{'console_scripts': ['yo = yo:main']}

setup_kwargs = {
    'name': 'yo-runner',
    'version': '0.1.1',
    'description': 'A YAML-driven task runner for lazy people',
    'long_description': "# Yo-runner\n\nYo is a Yaml-driven task runner for lazy people. When you're coding, you may\noften need to run a long command many times, but you don't want to do all that\ntyping every time. You don't want to have to remember the options or the flags\nevery time. You could write a Makefile, but they're annoying. Maybe your\ntoolkit provides the functionality, if you want to mess with that. You could\nuse something like gulp or grunt, but that's a lot of overhead. All you really\nwant is something like directory-specific aliases.\n\nThat's where yo comes in. All you do is write a `yo.yaml` that looks something\nlike this:\n\n``` {.yaml}\nrun: poetry run flask run\nserve-docs: python -m http.server --directory docs/_build\ndocs: \n  - poetry run sphinx-build docs docs/_build | tee docs/build_errors.txt\n  - serve-docs\ntest: poetry run pytest\n```\n\nNow, in that directory you can run `yo run` to run your app, `yo serve-docs` to\nserve your documentation folder, `yo docs` to build and serve documentation,\nand `yo test` to figure out why your stupid program still isn't working. And\nany arguments you pass to the `yo` command will be passed through the task.\n\nYo can handle single commands, sequential lists, and concurrent lists. Every\ncommand is run on the shell, so pipes and redirects work. There's also support\nfor environment variables and variables internal to the `yo.yaml` so that you\ndon't have to type paths more than once. It's lazy all the way down.\n\nSee the full documentation for yo at\n<https://OliverSherouse.github.io/yo-runner>.\n",
    'author': 'Oliver Sherouse',
    'author_email': 'oliver@oliversherouse.com',
    'url': 'https://github.com/OliverSherouse/yo-runner',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
