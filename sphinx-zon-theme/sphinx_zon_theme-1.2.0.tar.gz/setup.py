# This should be only one line. If it must be multi-line, indent the second
# line onwards to keep the PKG-INFO file format intact.
"""Sphinx Theme for ZEIT ONLINE
"""

from setuptools import setup, find_packages
import os.path


def project_path(*names):
    return os.path.join(os.path.dirname(__file__), *names)


setup(
    name='sphinx_zon_theme',
    version='1.2.0',

    install_requires=[
        'sphinx_rtd_theme',
        'setuptools',
    ],

    entry_points={
        'sphinx.html_themes': [
            'sphinx_zon_theme = sphinx_zon_theme',
        ],
    },

    author='Wolfgang Schnerring <wolfgang.schnerring@zeit.de>',
    author_email='wolfgang.schnerring@zeit.de',
    license='MIT',
    url='https://github.com/zeitonline/sphinx_zon_theme/',

    keywords='',
    classifiers="""\
License :: OSI Approved :: MIT License
Programming Language :: Python
Programming Language :: Python :: 2
Programming Language :: Python :: 3
Framework :: Sphinx
Framework :: Sphinx :: Theme
"""[:-1].split('\n'),
    description=__doc__.strip(),
    long_description='\n\n'.join(open(project_path(name)).read() for name in (
        'README.rst',
        'CHANGES.txt',
    )),

    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
)
