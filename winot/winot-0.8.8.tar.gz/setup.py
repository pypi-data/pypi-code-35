import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="winot",
    version="0.8.8",
    author="Qantom Software Private Limited",
    author_email="info@qantom.com",
    description="WiNoT Wrappers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.qantom.com/winot_trainer.html",
    license="GNU General Public License v3 (GPLv3)", 
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)