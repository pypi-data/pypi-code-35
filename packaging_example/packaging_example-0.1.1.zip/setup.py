from setuptools import setup
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

setup(name='packaging_example',

      version='0.1.1',
      description='Example on packaging in Python3',

      url='https://github.com/geowatson/packaging-example',

      author='George Poputnikov',
      author_email='g.poputnikov@innopolis.ru',

      license='MIT',

      packages=['packaging_example', 'a'],
      zip_safe=False)
