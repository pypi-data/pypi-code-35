from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='linkinvclient',
      version='1.1',
      description='python and cli Client for providing  access to micros1 microservice after authtication from tokenleader',
      long_description=readme(),
      url='https://github.com/microservice-tsp-billing/linkinvclient',
      author='Bhujay Kumar Bhatta',
      author_email='bhujay.bhatta@yahoo.com',
      license='Apache Software License',
      packages=find_packages(),
#       package_data={
#         # If any package contains *.txt or *.rst files, include them:
#         '': ['*.txt', '*.rst', '*.yml'],
#         # And include any *.msg files found in the 'hello' package, too:
#         #'hello': ['*.msg'],
#     },
      include_package_data=True,
      install_requires=[
          'requests==2.20.1',
          'configparser==3.5.0',
          'PyJWT==1.7.0',
          'PyYAML==3.13',
          'cryptography==2.3.1',
          'six==1.11.0',
          'Flask==1.0.2',
          'Flask-Testing==0.7.1',
          'tokenleaderclient==1.3'
      ],
      entry_points = {
        'console_scripts': ['linkinv=linkinvclient.cli_parser:main',
                            ],
        },
      test_suite='nose.collector',
      tests_require=['nose'],

      zip_safe=False)
