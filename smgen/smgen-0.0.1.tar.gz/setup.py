import setuptools
V="0.0.1"
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="smgen",
    version=V,
    author="phoenix.lv",
    author_email="phoenix.grey0108@gmail.com",
    description="lib and code generator to create state machine app",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hellstein/statemachine",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
