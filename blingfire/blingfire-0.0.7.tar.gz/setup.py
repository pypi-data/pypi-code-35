import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="blingfire",
    version="0.0.7",
    author="Bling",
    author_email="bling@microsoft.com",
    description="Python wrapper of lightening fast Finite State machine and REgular expression manipulation library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/microsoft/blingfire/",
    packages=['blingfire'],
    package_data={'blingfire':['libblingfiretokdll.so','blingfiretokdll.dll']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)