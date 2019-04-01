from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(name='brackets_closed',
      version='0.4',
      description='Checks if brackets are closed given a string',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='http://pypi.python.org/pypi/brackets_closed/0.1',
      author='Daniel Keighley',
      author_email='daniel.keighley@wpengine.com',
      license='WP',
      packages=['brackets_closed'],
      zip_safe=False)