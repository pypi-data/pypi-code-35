from setuptools import setup, find_packages

setup(
    name = "weios_mytest1",
    version = "0.1.0",
    keywords = ("pip", "weios_test1", "mage"),
    description = "time and path tool",
    long_description = "time and path tool",
    license = "MIT Licence",

    url = "https://github.com/weios001/weios_mytest.git",
    author = "weios",
    author_email = "weios@woodcol.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = []
)
