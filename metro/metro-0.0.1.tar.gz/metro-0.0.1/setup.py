import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="metro",
    url="https://github.com/yourhiro/metro",
    author="Insert Overwrite",
    packages=["metro"],
    install_requires=["apache-airflow"],
    version="0.0.1",
    license="Apache License 2.0",
    description="Metro framework for Airflow",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
