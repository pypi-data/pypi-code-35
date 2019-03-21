import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="repository-flyingpeter",
    version="0.0.1",
    author="flyingpeter",
    author_email="pedroand@hotmail.com",
    description="Useful Stuff",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/flyingpetet/repository",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        ],
)
