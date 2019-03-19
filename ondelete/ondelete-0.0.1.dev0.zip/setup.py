from setuptools import setup
from ondelete._version import __version__

with open('README.md') as fid:
    LONG_DESCRIPTION = fid.read()

setup(
    name='ondelete',
    version=__version__,
    author='Roger D. Serwy',
    author_email='roger.serwy@gmail.com',
    license="BSD License",
    keywords="",
    url="http://github.com/serwy/ondelete",
    packages=['ondelete'],
    description='',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    platforms=["Windows", "Linux", "Solaris", "Mac OS-X", "Unix"],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
    ],
)
