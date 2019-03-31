#!/usr/bin/env python
# https://setuptools.readthedocs.io/en/latest/setuptools.html
from pathlib import Path

from setuptools import find_packages, setup

package = 'ChromeDevTools'
cur_dir = Path(__file__).parent
with open((cur_dir / 'README.md').resolve()) as f:
  readme = f.read()

# $ pip install -U ChromeDevTools
# Collecting ChromeDevTools
#   Using cached https://files.pythonhosted.org/packages/4f/9e/c61c5f3a4a383d2c14ca49f9b9bd37e6d8d62c8f9c7ce289a13fcc35b11c/ChromeDevTools-0.2.2.tar.gz
#     Complete output from command python setup.py egg_info:
#     Traceback (most recent call last):
#       File "<string>", line 1, in <module>
#       File "/tmp/pip-install-vy5q9y9g/ChromeDevTools/setup.py", line 12, in <module>
#         with open((cur_dir / 'LICENSE').resolve()) as f:
#     FileNotFoundError: [Errno 2] No such file or directory: '/tmp/pip-install-vy5q9y9g/ChromeDevTools/LICENSE'
# with open((cur_dir / 'LICENSE').resolve()) as f:
#   license = f.read()

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
  # license=license,
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
