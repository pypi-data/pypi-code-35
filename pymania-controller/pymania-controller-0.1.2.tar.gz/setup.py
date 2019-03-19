import setuptools

from pymania import __version__ as version

with open('README.md', 'r') as readme:
    LONG_DESCRIPTION = readme.read()

setuptools.setup(
    name='pymania-controller',
    version=version,
    author='v7a',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/v7a/pymania',
    packages=setuptools.find_packages(),
    install_requires=["defusedxml", "sqlalchemy"],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
