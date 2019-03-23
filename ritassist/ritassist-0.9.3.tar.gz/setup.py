from setuptools import setup

setup(name='ritassist',
      version='0.9.3',
      description='RitAssist API Access',
      url='http://github.com/depl0y/ritassist-py',
      author='Wim Haanstra',
      author_email='wim@wim.me',
      license='MIT',
      packages=['ritassist'],
      install_requires=[
          'requests',
          'ciso8601',
          'geopy',
          'sseclient'
      ],
      python_requires='>=3',
      zip_safe=False)