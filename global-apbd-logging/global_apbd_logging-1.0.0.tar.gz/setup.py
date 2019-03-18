from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="global_apbd_logging",
    version="1.0.0",
    description="A Python package to get log of apbd.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/adityayudhi/global_apbd_logging",
    author="Aditya Yudhi Hanafi",
    author_email="adityayudhi10@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["global_apbd_logging"],
    include_package_data=True,
    install_requires=["httpagentparser", "get-mac"],
    entry_points={
        "console_scripts": []
    },
)