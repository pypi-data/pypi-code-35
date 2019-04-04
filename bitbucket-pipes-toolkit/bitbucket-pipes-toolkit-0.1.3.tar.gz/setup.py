from setuptools import setup

setup(
    name='bitbucket-pipes-toolkit',
    version='0.1.3',
    packages=['bitbucket_pipes_toolkit', ],
    url='https://bitbucket.org/bitbucketpipelines/pipes-tools-python/src',
    author='Atlassian',
    author_email='bitbucketci-team@atlassian.com',
    description='This package containes various helpers for developing bitbucket pipelines pipes',
    long_description=open('README.md').read(),
    install_requires=['colorama==0.3.9',
                      'colorlog==4.0.2']
)
