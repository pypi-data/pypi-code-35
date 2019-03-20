import setuptools


def readme():
    with open("README.rst", "rt") as readme:
        return readme.read()


setuptools.setup(
    name="thewhitetools",
    version="0.0.3",
    author="Enrique Blanco Carmona",
    author_email="enblacar1996@gmail.com",
    description="A collection of functions and classes that come in handy for bioinformaticians.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/enblacar/thewhitetools",
    packages=setuptools.find_packages(),
    test_suite="nose.collector",
    tests_require=['nose'],
    scripts=[
        'bin/thewhitetools-joke',
    ],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Development Status :: 3 - Alpha',
    ],
    install_requires=[
        'markdown',
    ],
    entry_points={
        'console_scripts': ['thewhitetools-joke=thewhitetools.command_line:main'],
    },
    include_package_data=True,
    zip_safe=False,

)
