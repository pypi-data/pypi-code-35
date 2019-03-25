from setuptools import setup

import styled_log


def readme():
    with open('README.md', encoding="utf-8") as fp:
        return fp.read()


setup(
    name="styled_log",
    version=styled_log.__version__,
    description="logging.Formatter allowing for customized and colored logging output.",
    long_description=readme(),
    url="https://gitlab.com/ittVannak/styled-log",
    license=styled_log.__license__,
    author=styled_log.__author__,
    author_email="nickclawrence@gmail.com",
    py_modules=["styled_log"],
    install_requires=[
        'colorama'
    ],
    classifiers=[
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
