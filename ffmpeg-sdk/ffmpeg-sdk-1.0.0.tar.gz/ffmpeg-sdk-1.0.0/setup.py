from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='ffmpeg-sdk',
    version='1.0.0', 
    author="Truong cong Hoan Vu",
    author_email="kevin.truong.ds@gmail.com",
    description="ffmpeg package for heroku",
    long_description=long_description,
    url="http://www.elinkgate.com",
    packages=['ffmpeg'],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
