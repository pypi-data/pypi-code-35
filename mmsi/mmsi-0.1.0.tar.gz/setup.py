import setuptools

setuptools.setup(
    name="mmsi",
    version="0.1.0",
    author="Yuxin Dong",
    author_email="gamepiaynmo@gmail.com",
    description="Python wrapper for Modifiable Multi-Scale Image (MMSI) library.",
    long_description="The documentation can be found at https://bioai.gitlab.io/libMI-docs/",
    long_description_content_type="text/plain",
    url="https://gitlab.com/BioAI/libMI",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)