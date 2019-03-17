import os
from codecs import open
from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst'), 'r', 'utf-8') as handle:
    readme = handle.read()

setup(
    name='nameko-rediskn',
    version='0.0.1',
    description='Nameko Redis Keyspace Notifications extension.',
    author='Julio Trigo',
    author_email='julio.trigo@sohonet.com',
    url='https://github.com/sohonetlabs/nameko-rediskn',
    packages=find_packages(exclude=['test', 'test.*']),
    install_requires=[
        'redis>=2.10.5',
        'nameko>=2.11,<3',
    ],
    extras_require={
        'dev': [
            'pytest>=4.3.0',
            'flake8',
            'coverage',
            'restructuredtext-lint',
            'Pygments',
        ],
    },
    zip_safe=True,
    license='MIT License',
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Database",
        "Topic :: Database :: Front-Ends",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)
