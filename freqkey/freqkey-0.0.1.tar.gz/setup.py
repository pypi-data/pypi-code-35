import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="freqkey",
    version="0.0.1",
    author="Anshul Sirur",
    author_email="vixus0@gmail.com",
    description="Counts your keypresses",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vixus0/freqkey",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['inputs'],
    entry_points={
        'console_scripts': [
            'freqkey = freqkey.__init__:main',
        ],
    },
)
