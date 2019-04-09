from setuptools import setup, find_packages

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(name='acgaws',
      version='0.2',
      description='Library for reusable aws code',
      long_description=long_description,
      url='http://github.com/AustinCloudGuru/acg-libraries',
      author='Mark Honomichl',
      author_email='mark@austincloud.guru',
      license='MIT',
      packages=find_packages(),
      install_requires=[
            "boto3",
            "awsretry"
      ],
      zip_safe=False,
      classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent"
      ]
      )
