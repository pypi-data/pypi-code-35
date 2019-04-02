import os
import re

from setuptools import setup, find_packages


def __get_version():
    with open("image_processor_client/__init__.py") as package_init_file:
        return re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', package_init_file.read(), re.MULTILINE).group(1)


requirements = [
    "aiohttp"
]

on_rtd = os.getenv('READTHEDOCS') == 'True'
if on_rtd:
    requirements.append('sphinxcontrib-napoleon')

extra_requirements = {
    'docs': [
        'sphinx==1.8.3'
    ]
}

setup(
    name="image_processor_client",
    version=__get_version(),
    url="https://github.com/thec0sm0s/image-processor-client",
    author="□ | The Cosmos",
    description="Asynchronous python client for image-processor server (https://github.com/thec0sm0s/image-processor).",
    long_description=open("README.md").read(),
    packages=find_packages(),
    install_requires=requirements,
    extras_require=extra_requirements,
    classifiers=[
            'Development Status :: 4 - Beta',
            'License :: OSI Approved :: MIT License',
            'Intended Audience :: Developers',
            'Natural Language :: English',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Topic :: Software Development :: Libraries',
            'Topic :: Internet',
            'Topic :: Utilities',
    ]
)
