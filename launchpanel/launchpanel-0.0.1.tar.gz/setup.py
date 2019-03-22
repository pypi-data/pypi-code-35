import setuptools


try:
    with open('README.md', 'r') as fh:
        long_description = fh.read()
except: 
    long_description = 'A python based action launcher interface'

setuptools.setup(
    name='launchpanel',
    version='0.0.1',
    author='Mike Malinowski',
    author_email='mike@twisted.space',
    description='A Qt based Ui for Launchpad',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/mikemalinowski/launchpanel',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)