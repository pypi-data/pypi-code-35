from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="file-editor",
    version="1.0.0",
    description="A python package to convert a image/pdf file to pdf/image file format",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/nikhilkumarsingh/weather-reporter",
    author="Manchikanti Santhosh",
    author_email="manchikantisanthosh@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["file_editor"],
    include_package_data=True,
    install_requires=["pdf2image"],
)
