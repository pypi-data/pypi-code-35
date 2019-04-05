import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt', 'r') as fh:
    requirements = fh.read().split('\n')

setuptools.setup(
    name="PWE_NB_Extension",
    version="0.0.4",
    author="Sahil Gupta",
    author_email="",
    description="A Notebook Extension for the Possible Worlds Explorer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/idaks/PWE-NB-Extension",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
