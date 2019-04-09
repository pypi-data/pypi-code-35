import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="thraxisgamespatterns",
    version="0.0.1dev",
    author="Zack Simon",
    author_email="zack.simon+thraxisgames@gmail.com",
    description="A series of python programming patterns to extend and ease implementation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=['application', 'enumeration',
              'eventhandling',
              'factories', 'listeners', 'patterns', 'rules', 'sorting', 'transforming'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
