import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bfilter",
    version="1.0.0",
    author="sysatom",
    author_email="sysatom@gmail.com",
    description="A Simple Bloom Filter for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sysatom/python-bloom-filter",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=('data structures', 'bloom filter', 'bloom', 'filter', 'probabilistic'),
    platforms=['any'],
    install_requires=['bitarray>=0.8.3', 'mmh3>=2.5.1'],
    test_suite="bfilter.tests",
    zip_safe=True
)
