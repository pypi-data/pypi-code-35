import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="feynLab_sensor_shield",
    version="1.3.2",
    author="FeynLab Technology, Inc.",
    author_email="social@feynlab.io",
    description="Python Library for FeynLab Sensor Shield",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://docs.feynlab.io/hardware-solutions/feynlab-sensor-shield",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
    ],
)
