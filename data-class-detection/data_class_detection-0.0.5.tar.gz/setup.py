import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="data_class_detection",
    version="0.0.5",
    author="qiaowang",
    author_email="adawq0@gmail.com",
    description="A library for data class detection",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/w2qiao",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    install_requires=['grpcio', 'numpy', 'tensorflow', 'tensorflow-serving-api', 'antlr4-python3-runtime']
)
