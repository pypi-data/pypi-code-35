from setuptools import setup

setup(name='zbspy',
      version='0.16.2',
      description='Python Library for Interacting with the 0bsnetwork',
      url='http://github.com/0bsnetwork/zbspy',
      author='James Hitchcock',
      author_email='james@0bsnetwork.com',
      license='MIT',
      packages=['zbspy'],
      keywords = ['0bsnetwork', 'blockchain', 'analytics'],
      install_requires=[
	    'base58==0.2.5',
            'pyblake2',
            'python-axolotl-curve25519',
            'requests'
      ]
      )
