import setuptools
import sys

script_paths = [
    'bin\pystack.bat',
    'bin\pystack'
]

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='pystack_cli',
    version='1.0.2',
    author='Zoltan Csontos',
    author_email='zoltan.csontos.dev@gmail.com',
    description='PyStack micro-framework command line interface',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/zoltancsontos/pystack.sh-cli',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    scripts=script_paths
)
