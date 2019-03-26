# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['dunamai']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dunamai',
    'version': '0.2.0',
    'description': 'Dynamic version generation',
    'long_description': '\n# Dunamai\n\nDunamai is a Python 3.5+ library for producing dynamic version strings\ncompatible with [PEP 440](https://www.python.org/dev/peps/pep-0440).\n\n## Usage\n\nInstall with `pip install dunamai`, and then use as a library:\n\n```python\nfrom dunamai import Version\n\n# Assume that `git describe --tags --long --dirty`\n# outputs `v0.1.0rc5-44-g644252b-dirty`.\nversion = Version.from_git_describe(flag_dirty=True)\n\nassert version.serialize(with_metadata=True) == "0.1.0rc5.post44.dev0+g644252b.dirty"\nassert version.base == "0.1.0"\nassert version.epoch is None\nassert version.pre_type == "rc"\nassert version.pre_number == 5\nassert version.post == 44\nassert version.dev == 0\nassert version.commit == "g644252b"\nassert version.dirty\n```\n\nThe `serialize()` method gives you an opinionated, PEP 440-compliant default\nthat ensures that prerelease/postrelease/development versions are compatible\nwith Pip\'s `--pre` flag. The individual parts of the version are also available\nfor you to use and inspect as you please.\n\n## Comparison to Versioneer\n\n[Versioneer](https://github.com/warner/python-versioneer) is another great\nlibrary for dynamic versions, but there are some design decisions that\nprompted the creation of Dunamai as an alternative:\n\n* Versioneer has a CLI that generates Python code which needs to be committed\n  into your repository, whereas Dunamai is just a normal importable library.\n* Versioneer produces the version as an opaque string, whereas Dunamai provides\n  a Version class with discrete parts that can then be inspected and serialized\n  separately.\n* Versioneer provides customizability through a config file, whereas Dunamai\n  aims to offer customizability through its library API for scripting support\n  and use in other libraries.\n\n## Integration\n\n* Setting a `__version__`:\n\n  ```python\n  import dunamai as _dunamai\n  __version__ = _dunamai.get_version("your-library", third_choice=_dunamai.Version.from_git_describe).serialize()\n  ```\n\n* setup.py:\n\n  ```python\n  from setuptools import setup\n  from dunamai import Version\n\n  setup(\n      name="your-library",\n      version=Version.from_git_describe().serialize(),\n  )\n  ```\n\n* [Poetry](https://poetry.eustace.io):\n\n  ```python\n  import subprocess\n  from dunamai import Version\n\n  version = Version.from_git_describe()\n  subprocess.run("poetry run version {}".format(version))\n  ```\n\n  Or as an [Invoke](https://www.pyinvoke.org) task:\n\n  ```python\n  from invoke import task\n  from dunamai import Version\n\n  @task\n  def set_version(ctx):\n      version = Version.from_git_describe()\n      ctx.run("poetry run version {}".format(version))\n  ```\n\n## Development\n\nThis project is managed using Poetry. After cloning the repository, run:\n\n```\npoetry install\npoetry run pre-commit install\n```\n\nRun unit tests:\n\n```\npoetry run pytest --cov\npoetry run tox\n```\n',
    'author': 'Matthew T. Kennerly',
    'author_email': 'mtkennerly@gmail.com',
    'url': 'https://github.com/mtkennerly/dunamai',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
