from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(name='brackets_closed',
      version='0.9',
      description='Checks if brackets are closed given a string',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='http://pypi.python.org/pypi/brackets_closed/0.9',
      packages=find_packages('brackets_closed', exclude=['__pycache__', 'brackets_closed.egg-info']),
      author='Daniel Keighley',
      author_email='daniel.keighley@wpengine.com',
      license='WP',
      zip_safe=False)
