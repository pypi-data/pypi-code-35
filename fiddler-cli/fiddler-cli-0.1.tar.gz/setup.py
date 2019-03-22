import setuptools

with open('Readme.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='fiddler-cli',
    version='0.1',
    author='Fiddler Labs',
    description='CLI and tools for interacting with Fiddler Service',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://fiddler.ai',
    packages=setuptools.find_packages(),
    install_requires=['pandas>=0.2'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts': [
            'fiddler-cli = fiddler.cli:main',
            'fiddler = fiddler.cli:main',
            'fidl = fiddler.cli:main',
        ],
    },
)
