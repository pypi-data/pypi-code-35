import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="search_tools-bertof",
    version="0.0.2",
    author="Filippo Berto",
    author_email="berto.f@protonmail.com",
    description="A set of functions to simplify searches",
    long_description=long_description,
    # long_description_content_type="text/markdown",
    url="https://gitlab.com/bertof/search_tools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
