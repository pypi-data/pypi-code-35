from setuptools import setup

# reading long description from file
with open('DESCRIPTION.txt') as file:
    long_description = file.read()

# specify requirements of your package here
REQUIREMENTS = ['nltk']

# some more details
CLASSIFIERS = [
    'Development Status :: 1',
    'Intended Audience :: Developers and Users',
    'Topic :: Extraction',
    'License :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
]

# calling the setup function
setup(name='extract_time',
      version='1.0.0',
      description='This module helps you extract hour and minutes from a string in python.',
      long_description=long_description,
      url='https://github.com/yashiksingh9/extract_time',
      author='YASHIK KUMAR SINGH',
      author_email='yashiksingh@gmail.com',
      license='MIT',
      packages=['extract_time'],
      classifiers=CLASSIFIERS,
      install_requires=REQUIREMENTS,
      keywords='extract time hour minutes string text'
      )