import setuptools


setuptools.setup(
    name="blingfire",
    version="0.0.5",
    author="Bling",
    author_email="bling@microsoft.com",
    description="test package",
    packages=['blingfire'],
    package_data={'blingfire':['libblingfiretokdll.so','blingfiretokdll.dll']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)