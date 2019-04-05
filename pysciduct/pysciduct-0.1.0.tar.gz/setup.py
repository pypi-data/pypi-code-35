from setuptools import setup, find_packages

setup(
    name='pysciduct',
    version='0.1.0',
    description='Python wrapper classes for SciDuct api.',
    url='https://github.com/NSSAC/pysciduct.git',
    author='Matthew Wong',
    author_email='mttwong@vt.edu',
    license='Apache License 2.0',
    packages=find_packages(exclude=['docs', 'tests*', 'useful_scripts']),
    test_suite='tests',
    install_requires=[
        'requests',
        'pyjwt',
        'cryptography',
        'jsonschema',
    ],
)
