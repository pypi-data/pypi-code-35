from setuptools import setup

setup(name='qbx',
      author='qbtrade',
      url='https://github.com/qbtrade/qbx',
      author_email='admin@qbtrade.org',
      packages=['qbx'],
      version='2019.3.18.0',
      description='Qbtrade Management Script',
      install_requires=[
          'docopt',
          'requests',
          'flask',
          'flask_restful',
          'redis',
      ],
      zip_safe=False,
      entry_points={'console_scripts': ['qbx=qbx:run', 'qbs=qbx:qbs']}
      )
