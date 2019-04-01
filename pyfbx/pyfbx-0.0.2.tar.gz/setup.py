import pathlib
from setuptools import setup, find_packages

setup(
    name="pyfbx",
    version="0.0.2",
    description="Freebox thin client",
    long_description=(pathlib.Path(__file__).parent / "README.md").read_text(),
    long_description_content_type='text/markdown',
    author_email="teebeenator@gmail.com",
    url='https://framagit.org/sun/pyfbx',
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    packages=find_packages(),
    install_requires=["zeroconf", "requests"],
    include_package_data=True,
)
