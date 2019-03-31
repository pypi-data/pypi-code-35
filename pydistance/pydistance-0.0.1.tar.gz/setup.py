import os
from setuptools import setup

# Taken from https://github.com/kennethreitz/setup.py/blob/master/setup.py
here = os.path.abspath(os.path.dirname(__file__))

setup(
    name='pydistance',
    version='0.0.1',
    description='Package for plotting the closest point for a given set of coordinates',
    url='https://github.com/dang3r/pydistance',
    author='Daniel Cardoza',
    author_email='dan@danielcardoza.com',
    license='MIT',
    packages=['pydistance'],
    python_requires='>=3.4.0',
    scripts=['bin/pyd'],
    install_requires=['geopy', 'pytz', 'gmplot', 'click', 'googlemaps'],
    long_description='\n' + open(os.path.join(here, 'README.md')).read(),
    long_description_content_type='text/markdown',
    zip_safe=False
)