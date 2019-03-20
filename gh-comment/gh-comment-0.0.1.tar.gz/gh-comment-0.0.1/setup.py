from setuptools import setup

setup(
    name='gh-comment',
    version='0.0.1',
    description='publish comment to github pull request or issue.',
    author='wenning',
    scripts=['ghcomment'],
    install_requires=[
        'requests==2.21.0'
    ]
)