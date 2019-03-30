from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="zmq_cache",
    version="0.0.1",
    author="Yun Lu",
    author_email="luyun198993@gmail.com",
    description="Look aside cache implementation based on ZeroMQ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yunluyl/zmq_cache",
    install_requires=["pyzmq"],
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
