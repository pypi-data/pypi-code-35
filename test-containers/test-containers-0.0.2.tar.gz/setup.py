from test_containers.app import HELP_TEXT
import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="test-containers",
    version="0.0.2",
    author="Alassane Ndiaye",
    author_email="alassane.ndiaye@gmail.com",
    description=HELP_TEXT,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AlassaneNdiaye/test-containers",
    packages=setuptools.find_packages(),
    install_requires=[
        "docker",
        "PyYAML",
    ],
)
