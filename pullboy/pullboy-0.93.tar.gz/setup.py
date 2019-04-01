from setuptools import setup

__version__ = ['0.93']
with open('README.md', 'r') as fl:
    long_desc = fl.read()

setup(name='pullboy',
      version='.'.join(__version__),
      description='Super Simple Auto-Deployment server',
      long_description=long_desc,
      long_description_content_type='text/markdown',
      url='http://github.com/theSage21/pullboy',
      author='Arjoonn Sharma',
      author_email='arjoonn.94@gmail.com',
      packages=['pullboy'],
      install_requires=['bottle', 'pyyaml'],
      entry_points={'console_scripts': ['pullboy=pullboy:main']},
      keywords=['pullboy', 'auto deploy server'],
      zip_safe=False)
