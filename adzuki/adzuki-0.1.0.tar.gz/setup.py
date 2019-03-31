import setuptools

with open('README.md', 'r') as fh:
  long_description = fh.read()

setuptools.setup(
  name='adzuki',
  version='0.1.0',
  author='SHOWHUE, Ire Sun, Kunda Lee',
  author_email='ire7715+adzuki@hotmail.com',
  description='ORM for GCP datastore',
  long_description=long_description,
  long_description_content_type='text/markdown',
  url='https://github.com/showhue/adzuki/',
  packages=['adzuki'],
  classifiers=[
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
  ],
  install_requires=[
    'jsonschema>=3.0.1',
    'google-cloud-datastore>=1.7.3'
  ],
)
