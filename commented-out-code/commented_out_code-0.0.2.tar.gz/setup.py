import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="commented_out_code",
    version="0.0.2",
    author="qiaowang",
    author_email="adawq0@gmail.com",
    description="A helloworld test",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/w2qiao",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['grpc', 'tensorflow', 'tensorflow-serving-api']
)