import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dispyt",
    version="0.0.2b",
    author="truedl",
    author_email="dauzduz1@example.com",
    description="📚 Dispyt is an API wrapper for the Discord API [Python3] 📚",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/truedl/dispyt",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)