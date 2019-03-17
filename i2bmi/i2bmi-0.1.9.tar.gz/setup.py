import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="i2bmi",
    version="0.1.9",
    author="Sean C. Yu",
    author_email="Sean.Yu@WUSTL.edu",
    description="Biomedical Informatics toolkit by Institute for Informatics at Washington University School of Medicine in St. Louis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/abraxasyu/i2bmi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_data={
    '':['*'],
    }
)