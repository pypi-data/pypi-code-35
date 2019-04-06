from setuptools import setup
from setuptools.command.install import install
import os

DESC = "Python Client for debugserver-js"
URL = "https://github.com/tiflash/dsclient-py"
DOCS_URL = "https://dsclient-py.readthedocs.io"

AUTHOR = "Cameron Webb"
EMAIL = "webbjcam@gmail.com"

with open('README.rst') as f:
    long_description = f.read()

# Get version string from dsclient/version.py
_here = os.path.dirname(__file__)
# defines version_string
exec(open(os.path.join(_here, "dsclient", "version.py")).read())

setup(  name='dsclient',
        version=version_string, #@UndefinedVariable
        description=DESC,
        long_description=long_description,
        url=DOCS_URL,
        download_url=URL+'/tarball/'+version_string,
        author=AUTHOR,
        author_email=EMAIL,
        license='MIT',
        install_requires=[
        ],
        packages=["dsclient"],
        python_requires=">=2.7.13, <4",
        entry_points = {
        },
        include_package_data=True,
        zip_safe=False,
        classifiers = [
            "Development Status :: 5 - Production/Stable",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Topic :: Software Development :: Embedded Systems",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "Topic :: Software Development :: Testing",
            "Intended Audience :: Developers"
        ],
        project_urls = {
            'Documentation': DOCS_URL,
            'Source': URL,
        }

    )
