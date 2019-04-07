# -*- coding: utf-8 -*-

from setuptools import (setup, find_packages)

__VERSION__ = '1.0.0'
__AUTHOR__ = 'Way2enjoy (James)'
__AUTHOR_EMAIL__ = 'support@way2enjoy.com'

install_requires = [
    'Django',
    'Pillow',
    'requests',
    'way2E'
]

setup(
    name='django-image-optimizer-way2enjoy',
    version=__VERSION__,
    author=__AUTHOR__,
    author_email=__AUTHOR_EMAIL__,
    description='Django Image Optimizer (Compressor)',
    packages=find_packages(exclude=["*demo"]),
    include_package_data=True,
    zip_safe=False,
    url='https://github.com/way2enjoy2/django-image-optimizer-way2enjoy',
    download_url='https://github.com/way2enjoy2/django-image-optimizer-way2enjoy/tarball/v%s' % __VERSION__,
    keywords=['image optimizer', 'django image optimizer', 'image optimizer'],
    long_description=open('README.rst').read(),
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
    ],
    install_requires=install_requires,
)
