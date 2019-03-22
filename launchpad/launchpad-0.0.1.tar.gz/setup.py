import setuptools


try:
    with open('README.md', 'r') as fh:
        long_description = fh.read()
except: 
    long_description = 'A python based action launcher'

setuptools.setup(
    name='launchpad',
    version='0.0.1',
    author='Mike Malinowski',
    author_email='mike@twisted.space',
    description='A python based action launcher',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/mikemalinowski/launchpad',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)