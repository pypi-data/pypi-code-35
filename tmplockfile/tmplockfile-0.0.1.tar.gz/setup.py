import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tmplockfile",
    version="0.0.1",
    author="Leo Wallentin | J++ Stockholm",
    author_email="mejl@leowallentin.se",
    description="A minimal lock file mechanism",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jplusplus/lockfile",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
