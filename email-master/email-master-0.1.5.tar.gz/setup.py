from setuptools import setup


def parse_requirements(requirement_file):
    with open(requirement_file) as f:
        return f.readlines()


with open('./README.rst') as f:
    long_description = f.read()

setup(
    name='email-master',
    packages=['email_master'],
    version='0.1.5',
    description='Master Email Parsing Package',
    author='Swimlane',
    author_email="info@swimlane.com",
    long_description=long_description,
    install_requires=parse_requirements('./requirements.txt'),
    keywords=['utilities', 'email', 'parsing', 'eml', 'msg'],
    classifiers=[],
)
