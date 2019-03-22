from setuptools import setup, find_packages

setup(
    name="doggie",
    version="0.1.3",
    author="hujianxin",
    author_email="hujianxincn@foxmail.com",
    include_package_data=True,
    install_requires=find_packages(),
    license="Apache License",
    description="Python library for interacting to hbase shell",
)
