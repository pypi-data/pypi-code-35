from setuptools import setup

setup(
    name='hashget-kernel_org',
    version='0.4',
    description='kernel.org (linux kernel sources) plugin for hashget',
    long_description='kernel.org (linux kernel sources) plugin for hashget',
    author='Yaroslav Polyakov',
    author_email='yaroslaff@gmail.com',

    license='Apache Software License',

    packages=['hashget.heuristics.kernel_org'],
    zip_safe=False,
)

