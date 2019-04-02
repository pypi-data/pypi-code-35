import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tweetmanager-serpucga",
    version="1.1.5",
    author="Sergio Puche García",
    author_email="serpucga@protonmail.com",
    description="JSON to CSV converter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/Serbaf/tweet-manager.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
