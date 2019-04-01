import io
import setuptools as st
import sys

from setuptools.command.test import test as TestCommand

import seinfeld


class Tox(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
    def run_tests(self):
        import tox
        errno = tox.cmdline(self.test_args)
        sys.exit(errno)


with open('README.rst') as reader:
    readme = reader.read()


st.setup(
    name='seinfeld-lang',
    version=seinfeld.__version__,
    description='A programming language about nothing.',
    long_description=readme,
    author='Grant Jenks',
    author_email='contact@grantjenks.com',
    url='http://seinfeld-lang.com/',
    packages=['seinfeld'],
    package_data={'': ['LICENSE', 'README.rst']},
    tests_require=['tox'],
    cmdclass={'test': Tox},
    license='Apache 2.0',
    install_requires=[],
    classifiers=(
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
    ),
)
