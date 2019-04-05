import os

from setuptools import find_packages, setup

import datawok

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name=datawok.__package__,
    version=datawok.__version__,
    description="",
    url="https://github.com/The-Politico/django-datawok",
    author="POLITICO interactive news",
    author_email="interactives@politico.com",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Django",
        "Framework :: Django :: 2.0",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Internet :: WWW/HTTP",
    ],
    keywords="",
    packages=find_packages(exclude=["docs", "tests", "example"]),
    include_package_data=True,
    install_requires=[
        "python-dateutil",
        "psycopg2",
        "boto3",
        "django-postgres-copy",
    ],
    extras_require={"test": ["pytest"]},
)
