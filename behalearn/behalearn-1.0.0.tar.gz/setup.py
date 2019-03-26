import setuptools

VERSION = '1.0.0'

PKG_NAME = 'behalearn'
AUTHOR = 'Fastar'
AUTHOR_EMAIL = 'tp2018tim4@gmail.com'
with open('README.md', 'r') as f:
    LONG_DESCRIPTION = f.read()
URL = 'https://gitlab.com/tp-fastar/ml-module'

setuptools.setup(
    name=PKG_NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description='A set of python modules for behavioral data analysis',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url=URL,
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Operating System :: MacOS',
    ],
)
