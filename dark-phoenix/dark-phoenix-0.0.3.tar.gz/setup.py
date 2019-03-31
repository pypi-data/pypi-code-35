import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dark-phoenix",
    version="0.0.3",
    author="atv",
    author_email="andrevettickal@gmail.com",
    description="A test runner wrapping python unittest",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/test_framework/dark-phoenix.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
