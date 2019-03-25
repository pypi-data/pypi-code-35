import os
from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    name="django-admin-vali",
    version="0.1.7",
    author="Juan Carlo Henriques Junger",
    author_email="juancarlo.h.junger@hotmail.com",
    description="Django Admin with Vali theme",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JchJ/Vali-Django-Admin",
    classifiers=[
        'Programming Language :: Python',
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.1',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
