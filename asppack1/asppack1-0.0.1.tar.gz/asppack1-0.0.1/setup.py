import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="asppack1",
    version="0.0.1",
    author="sailesh",
    author_email="arjun_sailesh@yahoo.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aspadmanabhan/pythonrep/tree/master",
    packages=['D:\samplepackage\sampleapp'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
