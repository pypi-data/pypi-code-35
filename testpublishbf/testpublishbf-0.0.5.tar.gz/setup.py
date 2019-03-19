import setuptools


setuptools.setup(
    name="testpublishbf",
    version="0.0.5",
    author="jiamguo",
    author_email="jiamguo@microsoft.com",
    description="test package",
    packages=['blingfire'],
    package_data={'blingfire':['libblingfiretokdll.so','blingfiretokdll.dll']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)