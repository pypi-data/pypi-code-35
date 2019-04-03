import codecs
import os
import re

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    try:
        with codecs.open(os.path.join(here, *parts), 'r', encoding='gbk') as fp:
            return fp.read()
    except UnicodeDecodeError:
        with codecs.open(os.path.join(here, *parts), 'r', encoding='utf-8') as fp:
            return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]",
        version_file,
        re.M,
    )
    if version_match:
        return version_match.group(1)

    raise RuntimeError("Unable to find version string.")


long_description = read('README.md')

setup(
    name="syndir",
    version=find_version("syn_src", "__init__.py"),
    description="多目录文件同步",
    long_description=long_description,

    license='Apache License',
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    url='https://github.com/sixiyizai/syndir',
    keywords='synchronization directorys',
    author='sixi',
    author_email='',
    package_dir={"syndir": "syn_src"},
    packages=find_packages(),
    package_data={
    },
    entry_points={
        "console_scripts": [
            "syndir=syn_src.cmdline:execute",
        ],
    },

    zip_safe=False,
    python_requires='>=3.0.0',
)
