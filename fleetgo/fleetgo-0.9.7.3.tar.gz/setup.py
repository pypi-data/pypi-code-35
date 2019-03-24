from setuptools import setup

setup(name='fleetgo',
      version='0.9.7.3',
      description='FleetGO API Access',
      long_description='Simple library to have API access to the FleetGO cloud platform',
      url='http://github.com/depl0y/fleetgo-py',
      author='Wim Haanstra',
      author_email='wim@wim.me',
      license='MIT',
      packages=['fleetgo'],
      install_requires=[
          'ciso8601',
          'geopy',
          'certifi',
          'urllib3',
          'sseclient-py'
      ],
      python_requires='>=3',
      zip_safe=False)
