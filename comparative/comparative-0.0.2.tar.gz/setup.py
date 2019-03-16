import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="comparative",
    version="0.0.2",
    author="Ezekiel Naa Bukari",
    author_email="enbukari@gmail.com",
    description="Implement comparison magic methods in one line!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ebukari/comparative",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    py_modules = ["comparative"]
)
