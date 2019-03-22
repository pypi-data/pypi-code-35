#!/usr/bin/env python
import setuptools
# from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

package_dir = {
      'influxed': 'src/influxed', 
      'influxed.ifql': 'src/influxed/ifql',
      'influxed.ifql.line_protocol': 'src/influxed/ifql/line_protocol',
      'influxed.mediator': 'src/influxed/mediator',
      'influxed.mediator.client_wrappers': 'src/influxed/mediator/client_wrappers',
      'influxed.orm': 'src/influxed/orm',
      'influxed.orm.capabilities': 'src/influxed/orm/capabilities',
      'influxed.orm.columns': 'src/influxed/orm/columns',
      'influxed.orm.declarative': 'src/influxed/orm/declarative'
}
setuptools.setup(
      name='influxed',
      version='0.1.4',
      author='Emil S Roemer',
      author_email='emilromer@hotmail.com',
      description='Inlfuxed influx query language and orm',
      package_dir=package_dir,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://gitlab.com/Romeren/influxed/',
      # py_modules=['influxed.__init__'],
      packages=[k for k, _ in package_dir.items()],
      classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+) ",
            "Operating System :: OS Independent",
      ],
)