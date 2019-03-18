from setuptools import setup
import re
import os
import codecs
from setuptools.command.test import test as TestCommand
import sys

here = os.path.abspath(os.path.dirname(__file__))

class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to pytest")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ""

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import shlex
        import pytest
        self.pytest_args += " --cov=meshparty --cov-report html "\
                            "--junitxml=test-reports/test.xml"

        errno = pytest.main(shlex.split(self.pytest_args))
        sys.exit(errno)

def read(*parts):
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

with open('requirements.txt', 'r') as f:
    required = f.read().splitlines()
    print(required)

with open('test_requirements.txt', 'r') as f:
    test_required = f.read().splitlines()

dependency_links = []
del_ls = []
for i_l in range(len(required)):
    l = required[i_l]
    if l.startswith("-e"):
        dependency_links.append(l.split("-e ")[-1])
        del_ls.append(i_l)

        required.append(l.split("=")[-1])

for i_l in del_ls[::-1]:
    del required[i_l]

print(dependency_links)
print(required)

setup(
    version=find_version("meshparty", "__init__.py"),
    name='meshparty',
    description='a service to work with meshes',
    author='Sven Dorkenwald',
    author_email='svenmd@princeton.edu',
    url='https://github.com/sdorkenw/MeshParty.git',
    packages=['meshparty'],
    include_package_data=True,
    install_requires=required,
    setup_requires=['pytest-runner'],
    dependency_links=dependency_links,
    tests_require=test_required,
    cmdclass={'test': PyTest},
    )
