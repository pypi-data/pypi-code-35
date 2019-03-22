import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cfn-deploy",
    version="1.0.9",
    description="Cloudformation deployment helper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/snowyhydrodev/shl-cloudformation/src",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
