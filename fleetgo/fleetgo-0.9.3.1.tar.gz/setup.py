from setuptools import setup

setup(name='fleetgo',
      version='0.9.3.1',
      description='FleetGO API Access',
      url='http://github.com/depl0y/fleetgo-py',
      author='Wim Haanstra',
      author_email='wim@wim.me',
      license='MIT',
      packages=['fleetgo'],
      install_requires=[
          'requests',
          'ciso8601',
          'geopy',
          'sseclient'
      ],
      python_requires='>=3',
      zip_safe=False)
