from setuptools import setup

setup(
    name='sfmc-to-json',    # This is the name of your PyPI-package.
    version='0.2',                          # Update the version number for new releases
    scripts=['salesforce_to_json.py']                  # The name of your scipt, and also the command you'll be using for calling it
)