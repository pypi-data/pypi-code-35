from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='sdk-dominator',
    version='0.0.3',
    description='Reads and store user data to validate Sibyl Score',
    long_description=readme,
    author='Raphael Schubert',
    author_email='rfswdp@gmail.com',
    url='https://github.com/rfschubert/sdk-dominator',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=[
        'pycpfcnpj',
        'requests',
        # 'environs',
        # 'xmltodict',
        # 'pendulum',
    ],
)