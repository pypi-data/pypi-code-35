from setuptools import setup
from setuptools.command.install import install as _install
from setuptools.command.develop import develop as _develop
from setuptools import find_packages
import re
import sys
from subprocess import run

with open('requirements.txt') as f:
    requirements = [l.strip() for l in f]

with open('dependency_links.txt') as f:
    dependency_links = [l.strip() for l in f]

# filter non-standard requirements
reqexp = re.compile(r"[^\w><=\.\s-]")
nonstandard = list(filter(reqexp.search, requirements))
requirements = list(filter(lambda w: not(reqexp.search(w)), requirements))

if nonstandard:
    if sys.argv[1] != "clean":
        print("Non-standard requirements found. These will have to installed manually. The non-standard requirements are:")
        print(nonstandard)

with open("README.md", "r") as f:
    long_description = f.read()

with open("LICENSE.txt", "r") as f:
    license_text = f.read()

versionRegex = re.compile("\d+[.]\d+[.]\d+[^\s]*")
with open("CHANGELOG.md", "r") as f:
    for line in f:
        versionMatch = versionRegex.match(line)
        if versionMatch:
            version = versionMatch.group()
            break


class InstallWrapper(_install):

    def run(self):
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>")
        _install.run(self)
        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        self.execute(self._post_install, (),
                     msg="Running post install task")

    def _post_install(self):
        # TODO: check spacy file version SM/MD/LG
        print("Downloading en_core_web_sm")
        result = run(["python", "-m", "spacy", "link", "en_core_web_sm", "en"], capture_output=True)
        if result.returncode == 0:
            print(result.stdout)
        else:
            if result.stderr:
                print('Preprocess failed: ')
                print(result.stderr)
            print("Downloading en_core_web_sm failed, please run:\n'python -m spacy download en_core_web_sm'")


class DevelopWrapper(_develop):

    def run(self):
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>")
        _develop.run(self)
        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        self.execute(self._post_install, (),
                     msg="Running post install task")

    def _post_install(self):
        # TODO: check spacy file version SM/MD/LG
        print("Downloading en_core_web_sm")
        result = run(["python", "-m", "spacy", "link", "en_core_web_sm", "en"], capture_output=True)
        if result.returncode == 0:
            print(result.stdout)
        else:
            if result.stderr:
                print('Preprocess failed: ')
                print(result.stderr)
            print("Downloading en_core_web_sm failed, please run:\n'python -m spacy download en_core_web_sm'")


setup(
    name='gherkan',
    version=version,
    use_scm_version=True,
    description='NL to Gherkin format translation tool',
    long_description=long_description,
    author='Imitation Learning Group CIIRC CVUT',
    maintainer_email='radoslav.skoviera@cvut.cz',
    url='',
    download_url='',
    license=license_text,
    install_requires=requirements,
    dependency_links=dependency_links,
    include_package_data=True,
    # setup_requires=['setuptools_scm'],
    packages=find_packages(include=["tests"], exclude=["data"]),
    cmdclass={
        'install': InstallWrapper,
        'develop': DevelopWrapper
        },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Development Status :: 3 - Alpha",
        "Framework :: Flask",
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Natural Language :: Czech",
        "Natural Language :: English",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Human Machine Interfaces"
    ]
)
