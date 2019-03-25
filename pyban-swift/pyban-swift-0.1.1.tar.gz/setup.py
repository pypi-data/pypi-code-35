from setuptools import setup

requirements = [
    'pycountry'
]

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(name='pyban-swift',
      version='0.1.1',
      description='IBAN validation tool in Python',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/Imperatus/PyBan',
      author='Jurgen Buisman',
      author_email='jurgen@labela.nl',
      license='GNU General Public License v3.0',
      packages=['pyban'],
      zip_safe=False,
      install_requires=requirements)
