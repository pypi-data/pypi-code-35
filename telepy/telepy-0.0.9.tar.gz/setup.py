import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="telepy",
    version="0.0.9",
    author="eliko",
    author_email="author@example.com",
    description="Telegram bot library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/2411eliko/tele/blob/master",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],    
    packages=setuptools.find_packages(),
    install_requires = ["requests", "urllib3"]
)

