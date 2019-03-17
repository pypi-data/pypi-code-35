import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="msbase",
    version="0.0.4",
    author="Zhen Zhang",
    # author_email="",
    description="Base Library for Python for MySelf",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/izgzhen/msbase.py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
