from setuptools import setup

setup(
    name='pspring-aws',
    version='0.0.8',
    license='TBD',
    author='Vasudevan Palani',
    author_email='vasudevan.palani@gmail.com',
    url='https://github.com/vasudevan-palani/pspring-aws',
    long_description="README.md",
    packages=['pspringaws'],
    install_requires=['boto3>1.9','pspring>=0.0.1'],
    include_package_data=True,
    description="A framework to do a better development.",
)
