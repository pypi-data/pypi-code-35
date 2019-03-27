
import os

from setuptools import setup, find_packages


here = os.path.realpath(os.path.dirname(__file__))
print(here)


def parse_requirements(filename):
    """Read pip-formatted requirements from a file."""
    reqs = (line.strip() for line in open(filename))
    return [line for line in reqs if line and not line.startswith("#")]


def long_description():
    with open("README.md", "r") as fh:
        return fh.read()


install_requirements = parse_requirements(os.path.join(here, 'requirements.txt'))
print(install_requirements)
tests_require = parse_requirements(os.path.join(here, 'requirements-dev.txt'))
print(tests_require)

setup(
    name='wrapAPI',
    version='0.0.1',
    author='Denis Korytkin',
    author_email='dkorytkin@gmail.com',
    description='Requests wrapper for API testing',
    keywords=['API', 'API testing', 'requests testing', 'requests wrapper'],
    long_description=long_description(),
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=['tests', 'tests.*']),
    # zip_safe=False,
    install_requires=install_requirements,
    # url='https://xxx.com',
    test_suite='tests',
    tests_require=tests_require,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    extras_require={'test': tests_require},
)
