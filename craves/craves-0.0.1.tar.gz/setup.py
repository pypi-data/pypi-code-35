import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="craves",
    version="0.0.1",
    author="Craves Team",
    author_email="qiuwch@gmail.com",
    description="Craves: Controlling Robotic Arm with a Vision and Economic System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/qiuwch/craves",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
