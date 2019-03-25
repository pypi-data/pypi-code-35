from setuptools import setup

requirements = [
    'pycountry'
]


setup(name='pyban-swift',
      version='0.1',
      description='IBAN validation tool in Python',
      url='https://github.com/Imperatus/PyBan',
      author='Jurgen Buisman',
      author_email='jurgen@labela.nl',
      license='GNU General Public License v3.0',
      packages=['pyban'],
      zip_safe=False,
      install_requires=requirements)
