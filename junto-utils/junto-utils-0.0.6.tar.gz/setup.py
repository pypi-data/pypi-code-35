import setuptools
from pip.req import parse_requirements


# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements('requirements.txt', session='hack')

# reqs is a list of requirement
# e.g. ['django==1.5.1', 'mezzanine==1.4.6']
reqs = [str(ir.req) for ir in install_reqs]

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="junto-utils",
    version="0.0.6",
    author="Timofey Katalnikov",
    author_email="kattimofey@gmail.com",
    description="Utils for Junto projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/junto-team/JuntoUtils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=reqs
)
