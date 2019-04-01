from setuptools import setup, find_packages

readme = open('README.md')
long_description = readme.read()
readme.close()

setup(
    name='pkiexpress',
    version='1.4.1',
    author='Ismael Medeiros',
    author_email="IsmaelM@lacunasoftware.com",
    description='Classes to consume PKI Express',
    long_description=long_description,
    keywords='python pki express certificate digital signature x509',
    url='https://github.com/LacunaSoftware/PkiExpressPython',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Information Technology',
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        "Operating System :: OS Independent",
        'Topic :: Security',
        'Topic :: Security :: Cryptography',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    install_requires=[],
)
