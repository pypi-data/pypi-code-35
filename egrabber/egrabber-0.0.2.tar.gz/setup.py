import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="egrabber",
    version="0.0.2",
    author="hari",
    author_email="hari@example.com",
    description="testpack",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=["new"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
