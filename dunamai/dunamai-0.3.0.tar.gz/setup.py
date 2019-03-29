# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['dunamai']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['dunamai = dunamai.__main__:main']}

setup_kwargs = {
    'name': 'dunamai',
    'version': '0.3.0',
    'description': 'Dynamic version generation',
    'long_description': '\n# Dunamai\n\nDunamai is a Python 3.5+ library for producing dynamic version strings\ncompatible with [PEP 440](https://www.python.org/dev/peps/pep-0440).\n\n## Features\n\n* Supports non-setuptools-based projects, so no need for a setup.py.\n* Version control system support:\n  * Git\n  * Mercurial\n\n## Usage\n\nInstall with `pip install dunamai`, and then use as either a CLI:\n\n```bash\n$ dunamai --help\n\n# Display dynamic version from a detected version control system:\n$ dunamai from any\n0.2.0.post7.dev0+g29045e8\n\n# Or use an explicit VCS:\n$ dunamai from git --no-metadata\n0.2.0.post7.dev0\n```\n\nOr as a library:\n\n```python\nfrom dunamai import Version\n\n# If `git describe` says `v0.1.0` or `v0.1.0-0-g644252b`\nversion = Version.from_git()\nassert version.serialize() == "0.1.0"\n\n# Or if `git describe` says `v0.1.0rc5-44-g644252b-dirty`\nversion = Version.from_any_vcs()\nassert version.serialize() == "0.1.0rc5.post44.dev0+g644252b"\nassert version.serialize(with_metadata=False) == "0.1.0rc5.post44.dev0"\nassert version.serialize(with_dirty=True) == "0.1.0rc5.post44.dev0+g644252b.dirty"\n```\n\nThe `serialize()` method gives you an opinionated, PEP 440-compliant default\nthat ensures that pre/post/development releases are compatible with Pip\'s\n`--pre` flag. The individual parts of the version are also available for you\nto use and inspect as you please:\n\n```python\nassert version.base == "0.1.0"\nassert version.epoch is None\nassert version.pre_type == "rc"\nassert version.pre_number == 5\nassert version.post == 44\nassert version.dev == 0\nassert version.commit == "g644252b"\nassert version.dirty\n```\n\n## Comparison to Versioneer\n\n[Versioneer](https://github.com/warner/python-versioneer) is another great\nlibrary for dynamic versions, but there are some design decisions that\nprompted the creation of Dunamai as an alternative:\n\n* Versioneer requires a setup.py file to exist, or else `versioneer install`\n  will fail, rendering it incompatible with non-setuptools-based projects\n  such as those using Poetry or Flit. Dunamai can be used regardless of the\n  project\'s build system.\n* Versioneer has a CLI that generates Python code which needs to be committed\n  into your repository, whereas Dunamai is just a normal importable library\n  with an optional CLI to help statically include your version string.\n* Versioneer produces the version as an opaque string, whereas Dunamai provides\n  a Version class with discrete parts that can then be inspected and serialized\n  separately.\n* Versioneer provides customizability through a config file, whereas Dunamai\n  aims to offer customizability through its library API and CLI for both\n  scripting support and use in other libraries.\n\n## Integration\n\n* Setting a `__version__` statically:\n\n  ```bash\n  $ echo "__version__ = \'$(dunamai from any)\'" > your_library/_version.py\n  ```\n  ```python\n  # your_library/__init__.py\n  from your_library._version import __version__\n  ```\n\n  Or dynamically (but Dunamai becomes a runtime dependency):\n\n  ```python\n  # your_library/__init__.py\n  import dunamai as _dunamai\n  __version__ = _dunamai.get_version("your-library", third_choice=_dunamai.Version.from_any_vcs).serialize()\n  ```\n\n* setup.py (no install-time dependency on Dunamai as long as you use wheels):\n\n  ```python\n  from setuptools import setup\n  from dunamai import Version\n\n  setup(\n      name="your-library",\n      version=Version.from_any_vcs().serialize(),\n  )\n  ```\n\n  Or you could use a static inclusion approach as in the prior example.\n\n* [Poetry](https://poetry.eustace.io):\n\n  ```bash\n  $ poetry version $(dunamai from any)\n  ```\n\n## Development\n\nThis project is managed using Poetry. After cloning the repository, run:\n\n```\npoetry install\npoetry run pre-commit install\n```\n\nRun unit tests:\n\n```\npoetry run pytest --cov\npoetry run tox\n```\n',
    'author': 'Matthew T. Kennerly',
    'author_email': 'mtkennerly@gmail.com',
    'url': 'https://github.com/mtkennerly/dunamai',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
