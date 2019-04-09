import setuptools
import haran_utils
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='haran_utils',
    version=haran_utils.__version__,
    author="Haran Rajkumar",
    author_email="haranrajkumar97@gmail.com",
    description="Certain utilities for various tasks",
    long_description_content_type="text/markdown",
    url="https://github.com/haranrk/",
    long_description=long_description,
    packages=setuptools.find_packages(),
    entry_points='''
        [console_scripts]
        utils=haran_utils.main:main
    ''',     
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],   
    
)