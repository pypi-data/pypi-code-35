from distutils.core import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
        name='pyqubole',
        version='0.1.5',
        author='Wesley Goi',
        author_email='picy2k@gmail.com',
        packages=['qubole'],
        scripts=['bin/qubole'],
        description='Managing qubole clusters',
        long_description=long_description,
        long_description_content_type='text/markdown'
)
