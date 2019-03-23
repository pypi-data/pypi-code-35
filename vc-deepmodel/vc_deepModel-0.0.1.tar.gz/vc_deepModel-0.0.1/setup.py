import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vc_deepModel",
    version="0.0.1",
    author="Kundjanasith Thonglek",
    author_email="thonglek.kundjanasith.ti7@is.naist.jp",
    description="Version Control of Computational Graph",
    long_description="Version COntrol of COmputational Graph (Neural Network)",
    long_description_content_type="text/markdown",
    url="https://github.com/Kundjanasith/vc-deepModel",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
