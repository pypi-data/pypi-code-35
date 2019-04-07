from setuptools import setup, find_packages

setup(
    name="NNstyle",
    version="0.0.2",
    keywords=("pip", "NNstyle", "NN-architecture"),
    description="draw neural network architecture",
    long_description="An interface to generate image of neural network architecture",
    license="MIT Licence",

    url="http://www.nanguoyu.com",
    author="nanguoyu",
    author_email="admin@nanguoyu.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["Pillow"]
)
