import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sqlite3-plus",
    version="0.0.3",
    author="doesdoing",
    author_email="doesdong@hotmail.com.com",
    description=open('README.md','r').read(),
    packages=setuptools.find_packages(),
)