#!/usr/bin/env python

from setuptools import setup

with open('dpd_static_support/version.py') as f:
    exec(f.read())

with open('README.md') as f:
    long_description = f.read()

setup(
    name="dpd-static-support",
    version=__version__,
    url="https://github.com/GibbsConsulting/dpd-static-support",
    description="Support for static assets in django-plotly-dash",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Mark Gibbs",
    author_email="dpd-static-support@gibbsconsulting.ca",
    license='MIT',
    packages=[
    'dpd_static_support',
    ],
    include_package_data=True,
    classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    ],
    keywords='django plotly plotly-dash dash dashboard django-plotly-dash',
    project_urls = {
    'Source': "https://github.com/GibbsConsulting/dpd-static-support",
    'Tracker': "https://github.com/GibbsConsulting/dpd-static-support/issues",
    'Documentation': 'http://django-plotly-dash.readthedocs.io/',
    },
    install_requires = [],
    python_requires=">=3.5",
    )

