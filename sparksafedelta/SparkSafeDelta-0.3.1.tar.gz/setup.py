from distutils.core import setup

setup(
    name='SparkSafeDelta',
    version='0.3.1',
    author='Aleksandrs Krivickis',
    author_email='aleksandrs.krivickis@gmail.com',
    packages=['sparksafedelta', 'sparksafedelta.tests'],
    # scripts=['bin/stowe-towels.py','bin/wash-towels.py'],
    url='http://pypi.python.org/pypi/SparkSafeDelta/',
    license='LICENSE.txt',
    description='Combination of tools that allow more convenient use of PySpark within Azure DataBricks environment.',
    long_description=open('README.md').read(),
    install_requires=[
                'pyspark',
          ],
)