import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="certibot",
    version="0.0.1",
    author="Systemico Software S.A.S",
    author_email="edwin.ariza@systemico.co",
    description="Script to validate the corporative or personal domains to get information about ssl certificates, and other more options.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/systemico/certibot",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)