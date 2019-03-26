# 1/usr/env/bin python
""" Class for creating a working environment.yml
for the conda environment, based on a list of R packages.

The class shall query information automatically accessing
the Anaconda cloud API for R packages living in
the 'r'-channel (CRAN packages) and 'bioconda'-channel
(i.e. Bioconductor).

R packages found in the 'r'-channel follow the scheme:
    r-<CRAN pkg name>
and for 'anaconda' it is:
    bioconductor-<bioconductor pkg name>
"""
import logging
import os
import requests

from ruamel.yaml import YAML
import click


class EnvBuilder(object):

    def __init__(self, rpackages, conda_env):
        """ Init the EnvBuilder object that is able 
        to read a R package list and tries to translate it
        to conda dependencies
        """
        self.failed = []
        self.warned = []
        self.passed = []
        self.resolved = {}
        self.conda_env = self.parse_conda_env(conda_env)
        self.rpackages = self.parse_package_list(rpackages)

    def build(self):
        """ Takes a list of R packages and tries to find the
        corresponding package in the Anaconda cloud
        and annotates it accordingly in the conda environment
        config file
        """
        check_functions = [
            'check_rpkgs',
            'extend_conda_env',
            'dump_conda_env'
        ]

        with click.progressbar(check_functions,
                               label='Running R package resolve tasks', item_show_func=repr) as fnames:
            for fname in fnames:
                getattr(self, fname)()
                if len(self.failed) > 0:
                    logging.error("Found test failures in '{}', \
                    halting lint run.".format(fname))
                    break

    def check_rpkgs(self):
        """ Check the rpackage list against the Anaconda cloud API """
        if not self.rpackages:
            self.warned.append((2, "The R package file seems to be empty."))
            return

        # Define the conda channels in which to search for R packages
        channels = {
            'r': 'r',
            'bioconda': 'bioconductor',
            'conda-forge': 'r'
        }

        for pkgInfo in self.rpackages:
            name, version = pkgInfo
            for channel in channels.keys():
                anaconda_url = "https://api.anaconda.org/package/{ch}/{pkg}".format(
                    ch=channel,
                    pkg="{prefix}-{pkg}".format(
                        prefix=channels.get(channel),
                        pkg=name.lower()
                    )
                )
                try:
                    resp = requests.get(anaconda_url, timeout=10)
                except (requests.exceptions.Timeout):
                    self.warned.append((2, "Server Timout! Package {pkg} could not be resolved.".format(
                        pkg=name.lower()
                    )))
                else:
                    if resp.status_code == 200:
                        body = resp.json()
                        available_versions = body["versions"]
                        if not version in available_versions:
                            self.warned.append((2, "No version {version} for package {name} on Anaconda cloud."
                                                   "\nOnly versions {version_list} are available".format(
                                version=version, name=name, version_list=available_versions)))
                            version = ""
                        self.resolved[name] = "{ch}::{prefix}-{pkg}{ver}".format(
                            ch=channel,
                            prefix=channels.get(channel),
                            pkg=name.lower(),
                            ver="={version}".format(version=version) if version else ""
                        )
                        self.passed.append(
                            ((2, "Package {pkg} resolved in channel {channel}".format(
                                pkg=name,
                                channel=channel
                            )))
                        )
                        break

        # Check for packages that could not have been resolved
        unresolved_pkgs = list([name for pkg, version in self.rpackages
                                if not self.resolved.get(pkg)])

        # And report them
        for pkg in unresolved_pkgs:
            self.warned.append((2,
                                "Could not resolve package {pkg} on Anaconda cloud.".format(
                                    pkg=pkg
                                )
                                ))

    def extend_conda_env(self):
        """ Take the resolved R packages and append them to the dependency
        list in the conda environment config """

        if not self.conda_env.get("dependencies"): self.conda_env["dependencies"] = []

        for pkg_ch_def in self.resolved.values():
            if not pkg_ch_def.split('::')[-1] in self.conda_env["dependencies"]:
                self.conda_env["dependencies"].append(pkg_ch_def.split('::')[-1])
                self.passed.append((3, "Added {pkg} to the conda dependency list.".format(
                    pkg=pkg_ch_def.split('::')[-1]
                )))

    def dump_conda_env(self):
        """ Dump the new conda config in the current working dir
        as a new environment.yml file """
        output = os.path.join(os.getcwd(), "environment.yml")
        with open(output, "w") as stream:
            yaml = YAML()
            yaml.indent(mapping=2, sequence=4, offset=2)
            yaml.dump(self.conda_env, stream)

    def parse_conda_env(self, conda_env):
        with open(conda_env, 'r') as stream:
            yaml = YAML()
            data = yaml.load(stream)
        return data

    def parse_package_list(self, rpackages):
        """ Parses a file with R package info and tries to find package and version.

        The input file format must have the keywords 'Package: <name>' followed by
        a new line with "Version: <version>", in order to find packages.

        Returns a list with tuples of package name and version.
        """
        packages = []
        with open(rpackages, 'r') as stream:
            content = stream.readlines()
        name, version = "", ""
        for line in content:
            if 'Package:' in line:
                try:
                    name = line.split(':')[1].strip()
                except Exception:
                    self.warned.append((1, "Could not parse Package info out of line:\n {}".format(line)))
            if 'Version:' in line:
                try:
                    version = line.split(':')[1].strip()
                except Exception:
                    self.warned.append((1, "Could not parse Package info out of line:\n {}".format(line)))
            if name and version:
                self.passed.append((1, "Found package \'{}\' with version \'{}\'.".format(name, version)))
                packages.append((name, version))
                name, version = "", ""
        if not packages:
            self.warned.append((1, "No packages have been parsed."))
        return packages

    def print_results(self):
        logging.info("===========\n BUILD RESULTS\n=================\n" +
                 "{0:>4} build steps passed".format(len(self.passed)) +
                 "{0:>4} build steps had warnings".format(len(self.warned)) +
                 "{0:>4} build steps failed".format(len(self.failed))
                 )
        if len(self.passed) > 0:
            logging.debug(
                "Test Passed:\n  {}".format("\n  ".join(["#{}: {}".format(eid, msg) for eid, msg in self.passed])))
        if len(self.warned) > 0:
            logging.warning(
                "Test Warnings:\n  {}".format("\n  ".join(["#{}: {}".format(eid, msg) for eid, msg in self.warned])))
        if len(self.failed) > 0:
            logging.error(
                "Test Failures:\n  {}".format("\n  ".join(["#{}: {}".format(eid, msg) for eid, msg in self.failed])))
