import setuptools
from os import path

with open("Readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='django-mdbsessions',
    version='0.0.2',
    author='somatoko',
    author_email='',
    description='Use MongoDB as Django session backend',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/somatoko/django-mdbsessions',
    zip_safe=False,
    packages=setuptools.find_packages(),
    install_requires=[
        'django >= 1.11',
        'pymongo >= 3.2.2'
    ],
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP :: Session',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='django mongodb session',
)
