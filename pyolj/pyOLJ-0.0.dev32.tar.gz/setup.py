from setuptools import setup, find_packages

setup(name='pyOLJ',
      version='0.0.dev32',
      description='AImageLab Code Judge for Python',
      url='https://github.com/aimagelab/pyOLJ',
      author='Lorenzo Baraldi',
      author_email='lorenzo.baraldi@unimore.it',
      packages=find_packages(exclude=('test', )),
      install_requires=[
          'numpy',
          'torch',
      ],
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: BSD License",
          "Operating System :: OS Independent",
      ])
