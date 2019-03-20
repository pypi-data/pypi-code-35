import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mysql-client",
    version="0.0.1",
    author="Jason Fried",
    author_email="me@jasonfried.info",
    description="A modern mysql client driver for modern python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fried/mysql-client",
    packages=setuptools.find_packages(),
    zip_safe=False,
    python_requires=">=3.7",
    license="MIT",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Cython",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Database",
        "Topic :: Database :: Database Engines/Servers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)

