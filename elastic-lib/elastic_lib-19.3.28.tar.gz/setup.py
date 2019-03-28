from setuptools import setup, find_packages

setup(name='elastic_lib',
      version='19.03.28',
      url='https://labola.jp',
      license='MIT',
      author='Luxeys',
      author_email='tessier@luxeys.com',
      description='Common elastic stuff for the projects.',
      long_description_content_type="text/markdown",
      packages=find_packages(),
      long_description=open('README.md').read(),
      zip_safe=False)
