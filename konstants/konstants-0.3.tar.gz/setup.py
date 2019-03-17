from setuptools import setup, find_packages

setup(
    name='konstants',
    version='0.3',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='Python package for common math and physics constants.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/thisisjustinm/constant-list',
    author='Justin M.',
    author_email='thisisjustinm@outlook.com'
)