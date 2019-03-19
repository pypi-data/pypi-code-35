import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="JPyTools",
    version="0.0.6",
    author="Jack Freund",
    author_email="jackkillian.on.scratch@gmail.com",
    description="A small collection of fun functions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Jackkillian/JPyTools",
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Development Status :: 2 - Pre-Alpha  ",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Topic :: Other/Nonlisted Topic",
    ],
    install_requires="requests",
    python_requires=">=3"
)
