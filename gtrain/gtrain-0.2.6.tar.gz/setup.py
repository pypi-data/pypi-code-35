import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='gtrain',
    version='0.2.6',
    description='Abstraction for general models in tensorflow with implemented train function',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://bitbucket.org/fantamat/gtrain', #todo move to github
    author='Matěj Fanta',
    author_email='fantamat93@gmail.com',
    license='MIT',
    packages=['gtrain'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering",
    ]
)
