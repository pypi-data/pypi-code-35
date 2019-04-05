import setuptools
import configparser

def get_install_requires():
    config = configparser.ConfigParser()
    config.read('Pipfile')
    packages = [k for k in config['packages']]
    return packages

with open("README.md", "r") as fh:
    long_description = fh.read()

SOURCE_DIR = 'src'

setuptools.setup(
    name="django-base-project",
    version="0.0.5",
    author="Jonathan Meier",
    author_email="jonathan.w.meier@gmail.com",
    description="A base django project containing commonly used functionality",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jonathanmeier5/base-django-project",
    packages=setuptools.find_packages(SOURCE_DIR),
    package_dir={'':'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=get_install_requires(),
)
