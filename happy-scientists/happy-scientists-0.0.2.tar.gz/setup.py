import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="happy-scientists",
    version="0.0.2",
    author="Eduardo Bustos",
    author_email="eduardobustosmiranda@hotmail.com",
    description="Library for generate funny random scientists names",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Bignone/happy-scientists",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)