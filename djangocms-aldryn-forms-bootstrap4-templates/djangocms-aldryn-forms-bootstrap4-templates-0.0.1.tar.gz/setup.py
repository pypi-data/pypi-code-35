# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from aldryn_forms_bs4_templates import __version__


setup(
    name='djangocms-aldryn-forms-bootstrap4-templates',
    version=__version__,
    description=open('README.md').read(),
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author='what.digital',
    author_email='mario@what.digital',
    packages=find_packages(),
    platforms=['OS Independent'],
    install_requires=[
        'django-cms',
        'aldryn-forms',
        'django-sekizai',
    ],
    download_url='https://gitlab.com/what-digital/djangocms-aldryn-forms-bootstrap4-templates/-/archive/{}/djangocms-aldryn-forms-bootstrap4-templates-{}.tar.gz'.format(
        __version__,
        __version__
    ),
    url='https://gitlab.com/what-digital/djangocms-aldryn-forms-bootstrap4-templates/tree/master',
    include_package_data=True,
    zip_safe=False,
)
