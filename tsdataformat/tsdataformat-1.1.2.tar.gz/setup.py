from setuptools import setup, find_packages
import re
import sys


VERSIONFILE="src/tsdataformat/_version.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))


url = 'https://github.com/ctberthiaume/tsdataformat-python'
download_url = url + '/archive/{}.tar.gz'.format(verstr)


setup(
    name='tsdataformat',
    version=verstr,
    author='Chris T. Berthiaume',
    author_email='chrisbee@uw.edu',
    license='MIT',
    description='A tool to validate and csv-ify a time series data format',
    long_description=open('README.rst', 'r').read(),
    url=url,
    download_url=download_url,
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    platforms='any',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only'
    ],
    keywords = ['csv', 'command-line', 'time series'],
    python_requires='>=3.0, <4',
    install_requires=[
        'click',
        'pendulum'
    ],
    zip_safe=True,
    entry_points={
        'console_scripts': [
            'tsdataformat2csv = tsdataformat:cli'
        ]
    }
)
