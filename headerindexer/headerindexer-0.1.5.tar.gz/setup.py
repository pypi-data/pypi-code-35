import setuptools

with open('README.md', 'r') as file:
    long_description = file.read()

setuptools.setup(
    name="headerindexer",
    version="0.1.5",
    author="Daniel Paz Avalos",
    author_email="me@dpazavalos.dev",
    description="A system to bind aliases to indexes of headers in a matrix",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dpazavalos/headerindexer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
