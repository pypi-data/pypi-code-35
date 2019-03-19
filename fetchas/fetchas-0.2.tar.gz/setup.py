import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(name='fetchas',
      version='0.2',
      description='Fetch web pages as robot',
      url='https://github.com/rosenhagen/fetchas',
      author='Henning Rosenhagen',
      author_email='hcodenhagen@gmail.com',
      long_description=README,
      long_description_content_type="text/markdown",
      packages=['fetchas'],
      install_requires=[
            'requests',
      ],
      entry_points={
            'console_scripts': [
                  'fetchas=fetchas.command_line:main',
                  'fetchas-mobile=fetchas.command_line:fetch_as_mobile',
            ],
      },
      classifiers=[
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.7",
      ],
      python_requires='>=3',
      zip_safe=False)
