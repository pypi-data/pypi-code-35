import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="solight-dy05",
    version="1.0.0",
    description="Control Solight DY05 sockets",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Funcoil/SolightDY05-PythonRpi",
    author="Martin Habovstiak",
    author_email="martin.habovstiak@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Home Automation",
        "Operating System :: POSIX :: Linux"
    ],
    packages=["dy05"],
    include_package_data=True,
    install_requires=["pigpio"],
    setup_requires=["pathlib"],
    entry_points={
        "console_scripts": [
            "dy05=dy05.__main__:main",
        ]
    },
)
