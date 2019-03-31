from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = ["pyperclip", "passlib", "cryptography"]

setup(
    name="simplepass",
    version="1.2.6",
    author="Jeff Moger",
    author_email="jeff-simple@moger.com",
    description="A simple password manager for the command line.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jeffmoger/pypass",
    packages=["simplepass"],
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    entry_points={
        'console_scripts': [
            'simple = simplepass.__main__:main',
        ],
    }
)
