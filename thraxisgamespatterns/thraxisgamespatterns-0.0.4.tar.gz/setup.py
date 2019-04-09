import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="thraxisgamespatterns",
    version="0.0.4",
    author="Zack Simon",
    author_email="zack.simon+thraxisgames@gmail.com",
    description="A series of python programming patterns to extend and ease implementation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_namespace_packages(include='thraxisgamespatterns.*'),
    classifiers=[
        "Programming Language :: Python :: 3",
        'License :: OSI Approved :: MIT License',
        "Operating System :: OS Independent",
    ],
)
