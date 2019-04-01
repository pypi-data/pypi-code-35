import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

packages = ['cheno',]


setup(name='cheno',
      version='0.1.3',
      description='Forward and Inverse Computation of Null Hypothesis Significance Tests.',
      long_description=README,
      long_description_content_type="text/markdown",
      url='https://github.com/RCoanda/lib-cheno',
      author='Radu-Andrei Coanda',
      author_email='radu.coanda@protonmail.com',
      license='MIT',
      packages=packages,
      package_dir={'cheno': 'cheno'},
      install_requires=[
          'numpy',
          'scipy',
      ],
      zip_safe=False,
      setup_requires=["pytest-runner"],
      tests_require=["pytest"],)
