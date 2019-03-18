from setuptools import setup
from setuptools import find_packages

setup(
    name='hellogoodbye',
    version='0.0.2',
    description='Hello, and good-bye!',
    author='Yusuke Sugomori',
    author_email='me@yusugomori.com',
    url='',
    download_url='',
    install_requires=[],
    classifiers=[
        'Development Status :: 1 - Planning'
    ],
    keywords='',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'hellogoodbye = hellogoodbye.__main__:main'
        ]
    }
)
