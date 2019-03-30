import os
from setuptools import setup, find_packages

import task_manager as package

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

setup(
    name="django-task-manager",
    version=package.__version__,
    description=package.__doc__.strip(),
    author=package.__author__,
    author_email=package.__email__,
    license=package.__license__,
    packages=find_packages(),
    long_description=README,
    long_description_content_type="text/markdown",
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Bug Tracking",
    ],
    include_package_data=True,
    zip_safe=False,
)
