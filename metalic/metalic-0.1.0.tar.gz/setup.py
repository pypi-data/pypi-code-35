from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='metalic',
    version='0.1.0',
    packages=['metalic'],
    url='https://github.com/JakeMakesStuff/Metalic',
    license='BSD-2-Clause',
    author='JakeMakesStuff',
    author_email='jake@gealer.email',
    setup_requires=required,
    description='Metalic is a open source library to create reactive web applications in Sanic.'
)
