import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vtemplate",
    version="0.0.1",
    author="sam-iau",
    author_email="sam-iau@outlook.com",
    description="A package to create the project directories in a structure",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/frier-sam/vtemplate",
    packages=setuptools.find_packages(),
    install_requires=[
      ],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)