"""
setup.py
~~~~~~~~~~~~~


:copyright: (c) 2016 Sander Bollen
:copyright: (c) 2016 Leiden University Medical Center
:license: MIT
"""
from os.path import abspath, dirname, join

from setuptools import setup, find_packages

readme_file = join(abspath(dirname(__file__)), "README.rst")
with open(readme_file) as desc_handle:
    long_desc = desc_handle.read()

setup(
    name="gvcf2bed",
    version="0.3.1",
    description="Convert gVCF into BED",
    long_description=long_desc,
    author="Sander Bollen",
    author_email="a.h.b.bollen@lumc.nl",
    url="https://github.com/sndrtj/gvcf2bed",
    license="MIT",
    packages=find_packages(),
    install_requires=["pyvcf==0.6.8", "cyvcf2>=0.7.4"],
    test_requires=["pytest", "pytest-cov"],
    entry_points={
        "console_scripts": [
            "gvcf2bed = gvcf2bed.gvcf2bed:main"
        ]
    },
    classifiers=[
        "Topic :: Scientific/Engineering :: Bio-Informatics"
    ]

)
