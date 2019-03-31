from codecs import open
from setuptools import setup

with open('flask_compressed/__init__.py', encoding='utf-8') as f:
    for line in f.readlines():
        if '__version__' in line:
            version = line.split("\"")[1]

setup(
    name='flask-compressed',
    version=version,
    description="",
    url='https://github.com/jeongukjae/flask-compressed',
    author='Jeong Ukjae',
    author_email='jeongukjae@gmail.com',
    license='MIT',
    packages=['flask_compressed'],
    classifiers=[
        "Development Status :: 3 - Alpha", "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7", "Topic :: Utilities"
    ])
