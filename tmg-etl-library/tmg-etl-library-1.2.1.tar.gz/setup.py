from setuptools import setup, find_packages
import version

with open('requirements.txt') as f:
    required = f.read().splitlines()

packages = find_packages()

setup(
    name='tmg-etl-library',
    version=version.__version__,
    description='TMG Etl library',
    author='Data Platform team',
    packages=find_packages(exclude=("tests","examples")),
    py_modules=['version'],
    package_data={},
    install_requires=required
)
