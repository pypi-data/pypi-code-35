import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="smartbee",
    version="0.1.4",
    author="Rhaniel Magalhães",
    author_email="rhaniel@alu.ufc.br",
    description="Biblioteca do projeto smartbee",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rhanielmx/smartbee",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
