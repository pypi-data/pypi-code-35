import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="test_chmod_xiaoxin",
    version="0.0.4",
    author="xiaoxin",
    author_email="xiaoxiaoxin6@163.com",
    description="test the right setting of the files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xiaoxiaoxin6/test_chmod_xiaoxin.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
