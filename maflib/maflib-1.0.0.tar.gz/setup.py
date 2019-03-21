from setuptools import find_packages, setup;

fd = open("README.rst");
long_description = fd.read();
fd.close();

setup(name              = "maflib",
      version           = "1.0.0",
      packages          = find_packages(),
      author            = "Samuel Li",
      author_email      = "sam@projreality.com",
      url               = "https://github.com/projreality/maflib",
      description       = "Library for reading and manipulating Mozilla Archive Format (MAF) files",
      long_description  = long_description,
      license           = "https://www.gnu.org/licenses/lgpl.html",
      install_requires  = [ "python-dateutil" ]
     );
