import os
import re
from setuptools import setup, find_packages


RE_PY_VERSION = re.compile(
    r'__version__\s*=\s*["\']'
    r'(?P<version>\d+(\.\d+(\.\d+)?)?)'
    r'["\']'
)


def read_version(path):
    content = read(path)
    m = RE_PY_VERSION.search(content)
    if not m:
        return '0.0'
    else:
        return m.group('version')


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="serafin-sqlalchemy",
    version=read_version('src/serafin_sqlalchemy/__init__.py'),
    author="Mateusz 'novo' Klos",
    author_email="novopl@gmail.com",
    license="MIT",
    keywords="serafin serialize sql sqlalchemy serialization json config",
    url="http://github.com/novopl/serafin-sqlalchemy",
    description="SQLAlchemy integration for serafin",
    long_description=read('README.rst'),
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=[
        "serafin>=0.12.0",
        'six>=1.0.0'
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
    ],
)
