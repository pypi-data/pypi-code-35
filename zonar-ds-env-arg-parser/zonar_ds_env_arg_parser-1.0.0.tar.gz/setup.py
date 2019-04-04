import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zonar_ds_env_arg_parser",
    version="1.0.0",
    author="Zonar Systems - Data Services Pod",
    author_email="DSPod@zonarsystems.com",
    keywords="zonar_ds_env_arg_parser",
    description="An argument helper used to validate environment variables",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/evcallia/zonar_ds_env_arg_parser.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
