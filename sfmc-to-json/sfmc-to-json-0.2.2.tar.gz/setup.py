from setuptools import setup

# This call to setup() does all the work
setup(
    name='sfmc-to-json',
    version="0.2.2",
    description="Used to format FuelSDK reponses into JSON",
    url="https://github.com/realpython/reader",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
    ],
    packages=["salesforce_to_json"],
    include_package_data=True,
    install_requires=["json", "suds"]
)