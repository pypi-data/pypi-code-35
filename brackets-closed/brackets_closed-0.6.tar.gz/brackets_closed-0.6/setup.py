from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(name='brackets_closed',
      version='0.6',
      description='Checks if brackets are closed given a string',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='http://pypi.python.org/pypi/brackets_closed/0.6',
      package_dir={'':'brackets_closed'},
      packages=find_packages('brackets_closed', exclude=['__pycache__']),
      author='Daniel Keighley',
      author_email='daniel.keighley@wpengine.com',
      license='WP',
      zip_safe=False)
