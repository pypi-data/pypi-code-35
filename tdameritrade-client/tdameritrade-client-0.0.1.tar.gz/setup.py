import setuptools
from tdameritrade_client import __version__

with open('README.md', 'r') as f:
    long_description = f.read()

requires=[
    'requests',
    'environs',
    'pytest-runner'
    ]

setuptools.setup(
    name='tdameritrade-client',
    version=__version__,
    author='Joe Castagneri',
    author_email='jcastagneri@gmail.com',
    description='A client for the TDA API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/tdameritrade-tools/tdameritrade-client',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    install_requires=requires,
    test_suite='pytest',
    tests_require=['pytest']
)
