from __future__ import absolute_import, division, print_function, unicode_literals

from setuptools import setup, find_packages
from distutils.util import convert_path

with open("README.rst", "r") as fh:
    long_description = fh.read()
with open("CHANGELOG.rst", "r") as fh:
    long_description = long_description + "\n\n" + fh.read()

if __name__ == '__main__':
    main_ns = {}
    ver_path = convert_path('netssh2/__init__.py')
    with open(ver_path) as ver_file:
        exec (ver_file.read(), main_ns)
    setup(name='netssh2',
          description='Library for communicating with network devices using ssh2-python.',
          long_description=long_description,
          long_description_content_type='text/x-rst',
          version=main_ns['__version__'],
          packages=find_packages(exclude=('selftests*',)),
          scripts=[],
          url='https://gitlab.com/jkrysl/netssh2',
          license='GPLv3',
          author='Jakub Krysl',
          author_email='jkrysl@redhat.com',
          install_requires=['ssh2-python'],
          classifiers=[
              "Development Status :: 3 - Alpha",
              "Programming Language :: Python",
              "Programming Language :: Python :: 2.7",
              "Programming Language :: Python :: 3.4",
              "Programming Language :: Python :: 3.5",
              "Programming Language :: Python :: 3.6",
              "Programming Language :: Python :: 3.7",
              "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
              "Operating System :: POSIX :: Linux",
              "Intended Audience :: Developers",
              "Intended Audience :: Education",
              "Intended Audience :: Science/Research",
              "Intended Audience :: System Administrators",
              "Topic :: Software Development :: Libraries",
              "Topic :: System :: Networking",
              "Topic :: System :: Shells"
          ],
          )
