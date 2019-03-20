#!/usr/bin/env python3

from setuptools import setup

# Work around mbcs bug in distutils.
# http://bugs.python.org/issue10945
import codecs
try:
    codecs.lookup('mbcs')
except LookupError:
    ascii = codecs.lookup('ascii')
    codecs.register(lambda name, enc=ascii: {True: enc}.get(name == 'mbcs'))

VERSION = '1.2.1'
URL = "https://github.com/quantadex/python-bitshares"

setup(
    name='quantadex',
    version=VERSION,
    description='Python library for quantadex',
    long_description=open('README.md').read(),
    download_url='{}/tarball/{}'.format(URL, VERSION),
    author='cryptoQuoc',
    author_email='quoc@quantadex.com',
    maintainer='cryptoQuoc',
    maintainer_email='quocble@gmail.com',
    url=URL,
    keywords=['bitshares', 'library', 'api', 'rpc'],
    packages=[
        "bitshares",
        "bitsharesapi",
        "bitsharesbase"
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Topic :: Office/Business :: Financial',
    ],
    install_requires=open("requirements.txt").readlines(),
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    include_package_data=True,
)
