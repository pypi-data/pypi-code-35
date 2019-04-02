#!/usr/bin/env python
# https://setuptools.readthedocs.io/en/latest/setuptools.html
from pathlib import Path

from setuptools import find_packages, setup

package = 'ChromeDevTools'
cur_dir = Path(__file__).parent
with open((cur_dir / 'README.md').resolve()) as f:
  readme = f.read()

with open((cur_dir / 'LICENSE').resolve()) as f:
  license = f.read()

about = {}
with open((cur_dir / package / 'version.py').resolve()) as f:
  exec(f.read(), about)

with open((cur_dir / 'requirements.txt').resolve()) as f:
  install_requires = f.read().splitlines()

setup(
  name=package,
  description='Async Chrome DevTools',
  long_description=readme,
  long_description_content_type='text/markdown',
  license=license,
  author=about['__author__'],
  author_email=about['__email__'],
  version=about['__version__'],
  url='https://github.com/codedumps/async-chrome-dev-tools',
  install_requires=install_requires,
  keywords='async chrome devtools',
  packages=find_packages(),
  # не помогло нахуй
  # data_files=[('', ['LICENSE'])],
  package_dir={package: package},
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Framework :: AsyncIO',
    'Topic :: Software Development :: Debuggers',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.7'
  ]
)
