from setuptools import setup,find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="Lab 3-Part2",
    version="0.0.1",
    author="Alireza Khodamoradi",
    author_email="akhodamo@ucsd.edu",
    description="This is our initial package for pip",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KastnerRG/pp4fpgas",
    packages=['Lab3-Part2'],
    include_package_data = True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_data={'Lab3-Part2':['*.bit','*.tcl','*.ipynb']},
    
)
