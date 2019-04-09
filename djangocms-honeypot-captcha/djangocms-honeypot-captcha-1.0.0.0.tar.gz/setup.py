# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from djangocms_honeypot_captcha import __version__


setup(
    name='djangocms-honeypot-captcha',
    version=__version__,
    description=open('README.md').read(),
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author='what.digital',
    author_email='mario@what.digital',
    packages=find_packages(),
    platforms=['OS Independent'],
    install_requires=[
        'django-cms>2',
        'aldryn-forms>=2',
    ],
    download_url='https://gitlab.com/what-digital/djangocms-honeypot-captcha/-/archive/{}/djangocms-honeypot-captcha-{}.tar.gz'.format(
        __version__,
        __version__
    ),
    url='https://gitlab.com/what-digital/djangocms-honeypot-captcha/tree/master',
    include_package_data=True,
    zip_safe=False,
)
