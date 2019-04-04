from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
      name='hexagdly',
      version='2.0.2',
      description='Utilising CNNs for hexagonally sampled data with PyTorch',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/ai4iacts/hexagdly',
      author='T.L. Holch, C. Steppa',
      author_email='holchtim@physik.hu-berlin.de, steppa@uni-potsdam.de',
      license = 'MIT',
      classifiers=[
            'Intended Audience :: Science/Research',
            'Topic :: Scientific/Engineering :: Image Recognition',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3.6',
            ],
      keywords='hexagonal convolution',
      packages=find_packages(),
      install_requires=['torch', 'torchvision', 'numpy'],
      python_requires='>=3.6',
      extras_require={
      'dev': ['scipy', 'matplotlib', 'jupyter', 'pytest']
      },
    )
