from setuptools import setup,find_packages

setup(name='webautomators',
version='0.3',
url='',
license='MIT',
author='Kaue Oliveira',
author_email='koliveirabn@indracompany.com',
description='Application Interaction Library with Web',
packages=['webautomators'],
install_requires=['selenium',"requests"],
zip_safe=True)