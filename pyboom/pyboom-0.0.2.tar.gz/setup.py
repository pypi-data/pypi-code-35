from setuptools import setup

setup(name='pyboom',
      version='0.0.2',
      description='Detonador de bombas .. boom!!!',
      long_description='Ejemplos para el tutorial - Doom presenta: Python desde cero',
      url='https://gitlab.com/geek.log/pyboom',
      author='constrict0r',
      author_email='constrict0r@protonmail.com',
      license='MIT',
      packages=['pyboom'],
      entry_points={
          'console_scripts': [
              'pyboom = pyboom.__main__:main'
          ]
      })
