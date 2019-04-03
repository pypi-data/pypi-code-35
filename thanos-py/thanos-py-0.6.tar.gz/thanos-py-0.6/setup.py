from setuptools import setup, find_packages
 
 
 
setup(name='thanos-py',
 
      version='0.6',
 
      url='https://github.com/cokia/thanos.py',
 
      license='MIT',
 
      author='h4nuko0n',
      
      python_requires  = '>=3',

 
      author_email='hwymaster01@hanukoon.com',
 
      description="😈When I'm done, half of files will still exist.",
 
      packages=find_packages(exclude=['tests']),
 
      long_description=open('README.md').read(),

      zip_safe=False)