import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()

requires = [
    'pathlib',
]

tests_require = [
    'pylint',
    'pytest',
    'pytest-cov',
    'Sphinx',
    'sphinx_rtd_theme',
    'wheel',
    'bumpversion',
]

setup(
    name='py_mini_sh',
    version='0.1.1',
    description='Python Mini Shell',
    long_description=README,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Utilities',
    ],
    author='Luke Tunmer',
    author_email='luke.tunmer@gmail.com',
    url='https://bitbucket.org/abelana/py_mini_sh',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    extras_require={
        'testing': tests_require,
    },
    install_requires=requires,
    entry_points={
    },
)
