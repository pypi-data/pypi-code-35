from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

def get_datafiles():
    return [("lib", ["lib/Bd.png", "lib/chromedriver_mac64", "lib/chromedriver_win32.exe", "lib/chromedriver_linux64"])]

setup(
    name="beepdrive",

    version="2019.3.25",

    description="Easily sync your PoliMi courses material locally.",

    long_description=long_description,

    long_description_content_type="text/markdown",

    url="https://github.com/amecava/beepdrive",

    author="Team 2 Quinti",

    author_email="amedeo.cavallo96@gmail.com",

    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],

    keywords="sample setuptools development",

    packages=find_packages(exclude=["contrib", "docs", "tests"]),

    python_requires=">=3.5",

    install_requires=[
        "selenium",
        "beautifulsoup4",
        "PyQt5",
        "qdarkstyle"
    ],

    data_files=get_datafiles(),

    entry_points={
        'console_scripts': [
            'beepdrive=beepdrive:main',
        ],
    },

    project_urls={
        "Bug Reports": "http://github.com/amecava/beepdrive/issues",
        "Source": "http://github.com/amecava/beepdrive",
    },
)

# python setup.py sdist
# twine upload --skip-existing dist/*

# set PATH=%PATH%;C:\Windows\System32\downlevel;
