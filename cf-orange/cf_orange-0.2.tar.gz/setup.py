from setuptools import setup, find_packages
import os

CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
]

dist = setup(
    name='cf_orange',
    version='0.2',
    author='Anze Vavpetic',
    description='Package providing Orange widgets for ClowdFlows 2.0',
    url='https://github.com/xflows/cf_orange',
    license='MIT License',
    classifiers=CLASSIFIERS,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Orange3==3.7.0',
        'liac-arff'
    ],
)
