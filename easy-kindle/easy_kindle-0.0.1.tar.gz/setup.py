from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
        author='Rounak Vyas',
        author_email='itsron143@gmail.com',
        name='easy_kindle',
        version="0.0.1",
        description='Send documents to kindle from the command line.',
        long_description=long_description,
        url='https://github.com/itsron717/easy-kindle',
        license='MIT',
        py_modules=['easy_kindle'],
        install_requires=[
            'click', 'stdiomask', 'appdirs'
            ],
        entry_points={
            'console_scripts': [
                'easy_kindle=easy_kindle:main',
                ]
            },
)