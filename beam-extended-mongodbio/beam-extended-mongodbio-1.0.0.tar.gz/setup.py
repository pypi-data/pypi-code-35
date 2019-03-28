import setuptools

# with open("../../README.md", "r") as fh:
#     long_description = fh.read()

setuptools.setup(
    name="beam-extended-mongodbio",
    version="1.0.0",
    description="Extend Apache Beam python API with new modules with no cursor timeout",
    # long_description=long_description,
    long_description_content_type="text/markdown",
    author="Kiagus Arief Adriansyah",
    author_email="kadriansyah@gmail.com",
    classifiers=(
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ),
    keywords=['Apache', 'Beam', 'python'],
    url="https://github.com/kadriansyah/beam-extended-mongodbio",
    packages=setuptools.find_packages(),
    install_requires=[
        'apache-beam',
        'pymongo'
    ]
)