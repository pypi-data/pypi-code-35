from distutils.core import setup
import versioneer

setup(
    name='SparkSafeDelta',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
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