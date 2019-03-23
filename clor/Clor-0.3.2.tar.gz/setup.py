try:
  from setuptools import setup
except ImportError:
  from distutils.core import setup


setup(
  name             = 'Clor',
  version          = '0.3.2',
  author           = 'saaj',
  author_email     = 'mail@saaj.me',
  packages         = ['clor'],
  test_suite       = 'clor.test',
  url              = 'https://bitbucket.org/saaj/clor',
  license          = 'LGPL-2.1+',
  description      = 'Application configuration via Python logging.config',
  long_description = open('README.rst', 'rb').read().decode('utf-8'),
  platforms        = ['Any'],
  keywords         = 'python configuration-management',
  classifiers      = [
    'Topic :: Software Development :: Libraries',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3 :: Only',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: Implementation :: CPython',
    'Intended Audience :: Developers'
  ]
)

