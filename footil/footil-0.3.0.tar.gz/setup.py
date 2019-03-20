from distutils.core import setup

setup(
    name='footil',
    version='0.3.0',
    packages=['footil'],
    license='LGPLv3',
    url='https://github.com/focusate/footil',
    description="Various Python helpers for other projects",
    long_description=open('README.rst').read(),
    install_requires=['yattag'],
    maintainer='Andrius Laukavičius',
    maintainer_email='dev@focusate.eu',
)
