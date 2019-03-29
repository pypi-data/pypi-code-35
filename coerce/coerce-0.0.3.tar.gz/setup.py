import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="coerce",
    version="0.0.3",
    author="Alastair McClelland",
    author_email="almcc.dev@gmail.com",
    description="A type hint coercion decorator.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/almcc/coerce",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["coerce"],
    extras_require={
        "dev": [
            "black==18.9b0",
            "invoke",
            "pytest",
            "pytest-black",
            "pytest-cov",
            "setuptools>=40.8.0",
            "twine",
            "wheel>=0.33.1",
        ]
    },
)
