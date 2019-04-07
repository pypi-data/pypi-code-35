import pathlib
from setuptools import setup

# The directory containing this file
Current = pathlib.Path(__file__).parent

# The text of the README file
README = Current.joinpath("README.md").read_text()

setup(
    name='PyAppCalc-2Simple',
    version='0.1',
    packages=['gui', 'Calcapp', 'CalcModel'],
    url='',
    license='MIT',
    author='kiki',
    author_email='kunal.shah1@gmail.com',
    description=''
)
