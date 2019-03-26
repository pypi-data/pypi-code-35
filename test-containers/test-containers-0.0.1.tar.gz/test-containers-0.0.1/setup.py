from test_containers import HELP_TEXT
import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="test-containers",
    version="0.0.1",
    author="Alassane Ndiaye",
    author_email="alassane.ndiaye@gmail.com",
    description=HELP_TEXT,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AlassaneNdiaye/test-containers",
    packages=setuptools.find_packages(),
)
