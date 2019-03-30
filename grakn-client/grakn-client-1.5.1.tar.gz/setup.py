from setuptools import setup
from setuptools import find_packages
from os import walk
from os.path import join


def create_init_files(directory):
    for dirName, subdirList, fileList in walk(directory):
        if "__init__.py" not in fileList:
            open(join(dirName, "__init__.py"), "w").close()

packages = find_packages()
for package in packages:
    create_init_files(package)
packages = find_packages()

setup(
    name = "grakn-client",
    version = "1.5.1",
    description = "Grakn Client for Python",
    long_description = open('README.md').read(),
    long_description_content_type="text/markdown",
    classifiers = ["Programming Language :: Python", "Programming Language :: Python :: 2", "Programming Language :: Python :: 2.7", "Programming Language :: Python :: 3", "Programming Language :: Python :: 3.4", "Programming Language :: Python :: 3.5", "Programming Language :: Python :: 3.6", "Programming Language :: Python :: 3.7", "Programming Language :: Python :: 3.8", "License :: OSI Approved :: Apache Software License", "Operating System :: OS Independent", "Intended Audience :: Developers", "Intended Audience :: Science/Research", "Environment :: Console", "Topic :: Database :: Front-Ends"],
    keywords = "grakn database graph knowledgebase knowledge-engineering",
    url = "https://github.com/graknlabs/grakn/tree/master/client-python",
    author = "Grakn Labs",
    author_email = "community@grakn.ai",
    license = "Apache-2.0",
    packages=packages,
    install_requires=["grpcio==1.16.0", "protobuf==3.6.1", "six==1.11.0", "enum-compat==0.0.2"],
    zip_safe=False,
)
