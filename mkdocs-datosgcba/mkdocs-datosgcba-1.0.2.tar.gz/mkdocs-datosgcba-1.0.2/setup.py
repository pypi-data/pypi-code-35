# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

VERSION = '1.0.2'

setup(
    name="mkdocs-datosgcba",
    version=VERSION,
    url='http://www.mkdocs.org',
    license='BSD',
    description='Temas de datosgcba para documentación con MkDocs',
    author='Buenos Aires Data',
    author_email='gobiernoabierto@buenosaires.gob.ar',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'mkdocs.themes': [
            'datosgcba_docs=datosgcba_docs'
        ]
    },
    zip_safe=False
)