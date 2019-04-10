import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wiki-archive-combsl10",
    version="0.0.5",
    author="Lucas Combs",
    author_email="l-combs@hotmail.com",
    description="An easy way to archive flash markdown pages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lcombs15/WikiArchive",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)