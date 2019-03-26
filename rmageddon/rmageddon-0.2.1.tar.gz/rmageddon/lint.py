#!/usr/bin/env python
""" Linting code for QBiC R analysis environment
checks.
"""
import os
import re
import logging

from ruamel.yaml import YAML
import click


class RContainerLint(object):
    """ Object that hold linting info and result """

    def __init__(self, pipeline_dir):
        """ Init the linting object """
        self.path = pipeline_dir
        self.conda_config = {}
        self.failed = []
        self.warned = []
        self.passed = []

    def lint_rproject(self):
        """ Main linting function.

        This function takes the R project directory and scans 
        it for different files/dirs and compares it
        against best practice rules we defined at QBiC for
        having an interoperable, reproducible R environment
        for bioinformatic analysis.

        Returns:
            dict: Summary of test result messages structured as follows:
            {
                'pass': [
                    ( test-id (int), message (string) ),
                    ( test-id (int), message (string) )
                ],
                'warn': [(id, msg)],
                'fail': [(id, msg)],
            }
        
         Raises:
            If a critical problem is found, an AssertionError is raised.
        """
        check_functions = [
            'check_files_exist',
            'check_dockerfile',
            'check_conda_environment'
        ]

        with click.progressbar(check_functions, label='Running R projects tests', item_show_func=repr) as fnames:
            for fname in fnames:
                getattr(self, fname)()
                if len(self.failed) > 0:
                    logging.error("Found test failures in '{}', halting lint run.".format(fname))
                    break

    def check_files_exist(self):
        """ Check, that files like Dockerfile and the conda
        environment.yml exists, and report a failing test, if not.
        Directories like 'data' and 'scripts' are obligatory for the moment, 
        and only a warning is raised, if they are not present """

        files_fail = [
            'Dockerfile',
            'environment.yml'
        ]
        files_warn = [
            'data',
            'scripts'
        ]

        for files in files_fail:
            if not os.path.isfile(self.pf(files)):
                self.failed.append((1, 'File {} not found.'.format(files)))
            else:
                self.passed.append((1, 'File {} found.'.format(files)))

        for files in files_warn:
            if not os.path.isdir(self.pf(files)):
                self.warned.append((1, 'Dir {} not found.'.format(files)))
            else:
                self.passed.append((1, 'Dir {} found.'.format(files)))

        if os.path.isfile(self.pf('environment.yml')):
            with open(self.pf('environment.yml'), 'r') as fh:
                yaml = YAML()
                self.conda_config = yaml.load(fh)

    def check_dockerfile(self):
        """ Check the Dockerfile not to be empty and fulfill
        some basic checks:
            - Building from r-base
            - Import of the rpackages.txt
            - Some labels present
        """

        with open(self.pf('Dockerfile')) as d_file:
            content = d_file.readlines()

        if not content:
            self.failed.append((2, 'Dockerfile seems to be empty.'))
            return

        labels = {}
        base_img = []
        environment_def = []

        for line in content:
            if 'LABEL' in line:
                line = line.strip()
                labelname = line.split('=')[0].strip().replace('LABEL ', '')
                labels[labelname] = line.split('=')[1].strip()
            if 'FROM' in line:
                line = line.strip()
                base_img.append(line)
            if 'environment.yml' in line:
                line = line.strip()
                environment_def.append(line)

        # 1. Evaluate the base image beeing from r-base
        if not base_img:
            self.failed.append((2, 'No base image was defined in the Dockerfile.'))
            return
        if any('continuumio/miniconda' in base for base in base_img[0].strip().split()):
            self.passed.append((2, 'Base image \'continuumio/miniconda\' was found in the Dockerfile.'))
        else:
            self.failed.append((2, 'Container is not build from \'continuumio/miniconda\' image'))
            return

        # 2. Evaluate the labels and if the required ones are present
        expected_labels = [
            'name',
            'maintainer',
            'version',
            'organization',
            'github'
        ]
        for label in expected_labels:
            if not any(label == x for x in labels.keys()):
                self.failed.append((2, 'You havent\'t set LABEL \'{}\' in the Dockerfile.'.format(label)))
                return

        # 3. Check if labels are empty
        for mand_label in expected_labels:
            if not labels[mand_label]:
                self.failed.append((2, "You did not provide content for label \'{}\' "
                                       "for your container.".format(mand_label)))
                return

        # 4. Check name matches regex
        name = r"(Q|q)[a-zA-Z0-9]{4}000_[a-zA-Z0-9]{1,15}_ranalysis"
        match = re.search(name, labels["name"])
        if not match:
            self.failed.append((2, "The container name was invalid. Make sure it "
                                   "matches the specification! Name was: {}".format(labels["name"])))
            return

        # 5. Check version matches regex
        sem_version = r"[0-9]*\.[0-9]*\.[0-9]*"
        match = re.search(sem_version, labels["version"])
        if not match:
            self.failed.append((2, "The version of the container was malformatted."
                                   " Be sure that you use semantic versioning <major>.<minor>.<patch> (https://semver.org/)"))
            return

        self.passed.append((2, 'All labels set correctly in the Dockerfile'))

    def check_conda_environment(self):
        """ Make some simple checks for the rpackages.txt,
        like raise a warning, if it is empty and fail, if there
        is more than one package listed per line.

        If there is such a thing as an RESTful API for CRAN/Bioconductor,
        we should test if the packages exist.
        """
        if not os.path.isfile(self.pf('environment.yml')): return

        # Define the mandatory conda declarations
        mand_conda_settings = [
            'name',
            'channels',
            'dependencies'
        ]
        # Define the mandatory conda channels (min. requirement)
        mand_channel_settings = [
            'defaults',
            'r'
        ]

        # Check that the mandatory conda env declarations are there
        for declaration in mand_conda_settings:
            if not self.conda_config.get(declaration):
                self.failed.append((3, "The conda env declaration \'{dec}\' is missing.".format(
                    dec=declaration
                )))
                return

        # Check the name regex
        # <projectcode>-ranalysis
        env_name = r"(Q|q)[a-zA-Z0-9]{4}000_[a-zA-Z0-9]{1,15}_ranalysis"
        match = re.search(env_name, self.conda_config.get('name'))
        if not match:
            self.failed.append((3, "The conda environment name was not set properly. \
            Make sure, it follows the guidelines."))
            return

        # Check that channels 'default' and 'r' are present
        missing_channels = list([ch for ch in mand_channel_settings
                                 if not ch in self.conda_config.get('channels')])

        for ch in missing_channels:
            self.failed.append((3, "Channel {ch} was not defined.".format(ch=ch)))
            return

        # Check that the dependency for r-base is there, and a version is set.
        rbase = list([basepkg for basepkg in self.conda_config.get("dependencies") if 'r-base' in basepkg])
        if not rbase:
            self.failed.append((3, "Could not find the \'r-base\' dependency."))
            return

        # Check that a version is given for the r-base pkg
        if not '=' in rbase[0]:
            self.failed.append((3, "Could not determine that \'r-base\' has a version tag."))
            return

        # Check that the version is numeric
        version = rbase[0].strip().split('=')[-1].replace('.', '')
        if not version.isdigit():
            self.failed.append((3, "The version tag \'{tag}\' was not numeric!".format(
                tag=rbase[0].strip().split('=')[-1]
            )))
            return

        self.passed.append((3, 'The conda environment seems to be OK.'))

    def pf(self, file_path):
        """ Quick path join helper method """
        return os.path.join(self.path, file_path)

    def print_results(self):
        logging.info("===========\n LINT RESULTS\n=================\n" +
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
