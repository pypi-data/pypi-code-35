"""
    Definition of YMLF distribution package
"""
import glob
from setuptools import setup

setup(
    name="ymlf",
    version="0.0.1",
    description="Command-line YAML parse and filtering",
    author="Simon A. F. Lund",
    author_email="safl@safl.dk",
    url="https://github.com/safl/ymlf",
    license="Apache License 2.0",
    install_requires=[
        "pyyaml (>=3.10)",
    ],
    zip_safe=False,
    data_files=[
        ("bin", glob.glob("bin/*")),
    ],
    options={"bdist_wheel":{"universal":True}},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Text Processing",
        "Topic :: Text Processing :: Filters",
        "Topic :: Text Processing :: Markup",
        "Topic :: Utilities"
    ],
)
