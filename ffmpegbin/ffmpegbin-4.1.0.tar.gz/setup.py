from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='ffmpegbin',
    version='4.1.0',
    author="Truong Cong Hoan Vu",
    author_email="kevin.truong.ds@gmail.com",
    description="ffmpeg package for pip",
    long_description=long_description,
    url="http://www.elinkgate.com",
    packages=['ffmpegbin'],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
