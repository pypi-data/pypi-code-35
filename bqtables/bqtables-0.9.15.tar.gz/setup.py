import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / 'README').read_text()

# This call to setup() does all the work
setup(
    name='bqtables',
    version='0.9.15',
    description='Wraps the Google Cloud API with a class designed for easy '
                'streaming inserts and updates.',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/sethlivingston/python-bq-client',
    author='Seth M. Livingston',
    author_email='webdevbyseth@gmail.com',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    packages=['bqtables'],
    include_package_data=True,
    install_requires=['google-cloud-bigquery'],
)
