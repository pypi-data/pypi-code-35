from setuptools import setup, find_packages

version = open('VERSION').read().strip()
license = open('LICENSE').read().strip()

setup(
    name='dtest-framework',
    version=version,
    license=license,
    author='Seth Jensen',
    author_email='sjensen85@gmail.com',
    url='https://github.com/sjensen85/dtest',
    description='A library to facilitate the testing of data inside data pipelines. Results are pushed to a messaging queue of some sort for consumption by applications, persistence, etc.',
    long_description=open('README.md').read().strip(),
    packages=find_packages(),
    install_requires=[
        # put packages here
        'six',
        'pika'
    ],
    test_suite='tests',
    entry_points={}
)
