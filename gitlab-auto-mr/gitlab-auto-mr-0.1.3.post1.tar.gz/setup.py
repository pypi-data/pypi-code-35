from setuptools import find_packages
from setuptools import setup

setup(name='gitlab-auto-mr',
      version='0.1.3.post1',
      description='A simple tool for automatically creating merge requests in GitLab',
      long_description=open("README.rst").read(),
      author='Haseeb Majid',
      author_email='me@haseebmajid.com',
      keywords='Python',
      license='Apache License',
      url='https://gitlab.com/hmajid2301/gitlab-auto-mr',
      python_requires='~=3.6',
      package_dir={'': 'src'},
      packages=find_packages(where='src'),
      zip_safe=False,
      include_package_data=True,
      install_requires=[
          "click>=7.0",
          "requests>=2.21.0",
      ],
      entry_points={
          'console_scripts': [
              'gitlab_auto_mr = gitlab_auto_mr.cli:cli'
          ]
      },
      classifiers=[
          'Programming Language :: Python',
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Topic :: Software Development :: Libraries :: Python Modules'
      ]
      )
