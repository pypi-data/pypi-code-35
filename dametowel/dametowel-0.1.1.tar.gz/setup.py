from distutils.core import setup

setup(
    name='dametowel',
    version='0.1.1',
    author='John M. Gabriele',
    author_email='jmg3000@gmail.com',
    packages=['dametowel', 'dametowel.test'],
    scripts=['bin/stowe-towels.py', 'bin/wash-towels.py'],
    url='http://pypi.python.org/pypi/dametowel/',
    license='LICENSE.txt',
    description='Useful towel-related stuff.',
    long_description=open('README.txt').read(),
)
