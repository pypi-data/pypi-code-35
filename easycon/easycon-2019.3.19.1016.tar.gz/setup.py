
import setuptools
#from setuptools import setup

setuptools.setup(
    name='easycon',
    scripts=['easycon', 'easycon.cmd'] ,
    version='2019.03.19.1016',
    author='Hengyue Li',
    author_email='hengyue.li@hengyue.li',
    packages=setuptools.find_packages(),
    license='LICENSE.md',
    description='A tool based on paramiko used to connect to remote server.',
    long_description=open('README.md',encoding="utf8").read(),
    long_description_content_type="text/markdown",
    install_requires=['asn1crypto==0.24.0', 'bcrypt==3.1.6', 'cffi==1.12.2', 'colorama==0.4.1', 'cryptography==2.4.2', 'HY-sshapi==2019.3.18.939', 'idna==2.7', 'paramiko==2.4.2', 'pyasn1==0.4.5', 'pycparser==2.19', 'PyNaCl==1.3.0', 'six==1.12.0', 'termcolor==1.1.0'],
)
