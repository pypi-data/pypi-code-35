import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='allelicimbalance',
    version='0.1.0',
    author='Anthony Aylward',
    author_email='aaylward@eng.ucsd.edu',
    description='Utilities for studying allelic imbalance',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/anthony-aylward/allelicimbalance.git',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    install_requires=['betabernsum', 'scipy']
)
