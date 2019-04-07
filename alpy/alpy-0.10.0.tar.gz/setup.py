import pathlib
import setuptools

setuptools.setup(
    name="alpy",
    version="0.10.0",
    description="Library for testing network virtual appliances using Docker",
    url="https://gitlab.com/abogdanenko/alpy",
    packages=["alpy"],
    author="Alexey Bogdanenko",
    author_email="alexey@bogdanenko.com",
    long_description=pathlib.Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: POSIX :: Linux",
    ],
)
