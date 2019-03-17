from distutils.core import setup

setup(
    name='SparkSafeDelta',
    version='0.1.9',
    author='Aleksandrs Krivickis',
    author_email='aleksandrs.krivickis@gmail.com',
    packages=['sparksafedelta', 'sparksafedelta.tests'],
    #scripts=['bin/stowe-towels.py','bin/wash-towels.py'],
    url='http://pypi.python.org/pypi/SparkSafeDelta/',
    license='LICENSE.txt',
    description='Tool that allows to automatically update schema of DataBricks Delta in case of Changes in data structure',
    long_description=open('README.txt').read(),
    install_requires=[
              'pyspark',
          ],
)