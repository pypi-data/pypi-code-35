from setuptools import setup

version = __import__('revoltsdk').__version__


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='revolt-sdk',
    version=version,
    python_requires='>=3.6',
    description='Client SDK for Revolt analytics',
    long_description=readme(),
    keywords='analytics revolt',
    url='https://www.revolt.rocks/',
    author='Miquido',
    author_email='contact@miquido.com',
    license='Apache 2.0',
    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: Apache Software License',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    packages=['revoltsdk'],
    zip_safe=False
)
