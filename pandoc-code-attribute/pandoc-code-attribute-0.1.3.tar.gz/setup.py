from setuptools import setup
from os import path
import pypandoc

version = '0.1.3'

repo_base_dir = path.abspath(path.dirname(__file__))

# Long description
readme = path.join(repo_base_dir, 'README.md')
long_description = pypandoc.convert(readme, 'rst')

setup(
    name='pandoc-code-attribute',
    version=version,
    description='Pandoc filter to add attributes to code blocks based on its class',
    long_description=long_description,
    author='DCsunset',
    author_email='DCsunset@protonmail.com',
    license='MIT',
    url='https://github.com/DCsunset/pandoc-code-attribute',
    
    install_requires=['panflute>=1'],
    # Add to lib so that it can be included
    py_modules=['pandoc_code_attribute'],
    entry_points={
        'console_scripts': [
            'pandoc-code-attribute = pandoc_code_attribute:main'
        ]
    },

    classifiers=[
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License'
    ]
)

