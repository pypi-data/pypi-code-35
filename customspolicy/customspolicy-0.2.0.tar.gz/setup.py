import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='customspolicy',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='',
    version='0.2.0',
    packages=setuptools.find_packages(),
    install_requires=[
    ]
)