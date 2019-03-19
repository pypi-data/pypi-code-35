"""
Copyright (c) 2019 LINKIT, The Netherlands. All Rights Reserved.
Author(s): Anthony Potappel

This software may be modified and distributed under the terms of the
MIT license. See the LICENSE file for details.
"""

import os
import re
import base64
import warnings

# pylint: disable=E0402
from . import gitconfig
from .system_execute import system_call
from .exceptions import ResponseError
from .validators import validate_url


class MakeGit():
    """Retrieve repository and sub-repositories, and merge these into a directory."""
    def __init__(self,
                 giturl=None,
                 build_directory='.',
                 verbose=False):

        (is_valid, error_message) = validate_url(giturl)
        if is_valid is False:
            raise ValueError(error_message)

        self.giturl = giturl
        self.build_directory = build_directory
        self.reponame = os.path.basename(re.sub(r'\.git$', '', giturl))
        self.pathname = self.build_directory + '/' + self.reponame
        self.verbose = verbose

        self.gitprefix = ['git', '-c', 'user.name=__auto_commit__', '-c', 'user.email=\'\'']

        if not os.path.isdir(self.build_directory):
            os.makedirs(self.build_directory)


    def git_command(self, command, pathname, allow_fail=False):
        """Internal error verification. Prints warning and/ or raises Exception"""
        return_code, stdout, stderr = system_call(command,
                                                  pathname=pathname,
                                                  verbose=self.verbose)
        if self.verbose is True:
            if stdout:
                print('\n'.join(stdout))
            if stderr:
                print('\n'.join(stderr))
        if allow_fail is True:
            return self

        if stderr:
            warnings.warn('\n'.join(stderr))
        if return_code != 0:
            raise ResponseError('git failed with return_code ' + str(return_code))
        return self

    def git_commit(self):
        """Commit all changes to git automatically"""
        self.git_command(self.gitprefix + ['add', '.'],
                         self.pathname, allow_fail=True)
        self.git_command(self.gitprefix + ['commit', '-m', '__auto_commit__:'],
                         self.pathname,
                         allow_fail=True)
        return self

    def pullmain(self):
        """Pull or clone a project into build_directory."""
        if not os.path.isdir(self.pathname):
            # directory not exist, assume clone
            pathname = self.build_directory
            command = self.gitprefix \
                      + ['clone', self.giturl, self.reponame]
        else:
            # assume pull
            pathname = self.pathname
            command = self.gitprefix + ['pull']

        self.git_command(command, pathname)
        return self

    def merge_submodules(self, remove_existing=False):
        """Fetch all configured repositories (main and sub), iterate through the
        list of submodules and include them in order."""
        # ensure .git/config is up-to-date (git fetch, and git read-tree depend on this
        self.remote_configuration()

        # load .gitmodules file as configparser configuration
        config = gitconfig.configparser_config(self.pathname + '/.gitmodules')
        if not isinstance(config, gitconfig.configparser.ConfigParser):
            return self

        # get all remotes
        remotes = gitconfig.remote_read(git_directory=self.pathname)
        if not isinstance(remotes, dict):
            return self

        # retrieve submodules fitting our pattern
        submodules = list([remote for remote in remotes.keys()
                           if re.match('^__submodule__[a-zA-Z0-9=]*$', remote)])

        if not submodules:
            return self

        # ensure all changes are committed to repository
        self.git_commit()

        # fetch modules
        self.git_command(['git', 'fetch', '--multiple'] + submodules,
                         self.pathname)

        for module_b64name in submodules:
            b64part = re.sub('^__submodule__', '', module_b64name)
            module_name = base64.standard_b64decode(b64part).decode()

            module_vars = gitconfig.section_dict(config,
                                                 'submodule',
                                                 module_name)
            if not isinstance(module_vars, dict) or module_vars.__len__() < 1:
                warnings.warn('submodule \'' + module_name + '\' has no variables set, skipping')
                continue

            module_path = module_vars.get('path')
            if not isinstance(module_path, str):
                warnings.warn('submodule \'' + module_name + '\' has no path set, skipping')
                continue

            if os.path.isdir(self.pathname + '/' + module_path):
                # directory exist, remove old first if allowed
                if remove_existing is True:
                    self.git_command(['git', 'rm', '-r', module_path],
                                     self.pathname)

            module_branch = module_vars.get('branch')
            if not isinstance(module_branch, str):
                # default to master branch
                module_branch = 'master'

            # activate module path
            self.git_command(['git', 'read-tree', '--prefix=' + module_path,
                              '-u', module_b64name + '/' + module_branch],
                             self.pathname)

        # ensure all changes are committed to repository
        self.git_commit()
        return self

    def add_remote(self, module_name, module_url):
        """Add a single remote project to .git/config
        used by self.update_remote()"""
        self.git_command(['git', 'remote', 'add', '-f', module_name, module_url],
                         self.pathname)
        return True

    def del_remote(self, module_name):
        """Delete a single remote project from .git/config
        used by self.update_remote()"""
        self.git_command(['git', 'remote', 'remove', module_name],
                         self.pathname)
        return True

    def remote_configuration(self):
        """Read .gitmodules to find remote sub-projects,
        and update .git/config accordingly to enable gitree"""
        module_file = self.pathname + '/.gitmodules'
        if not os.path.isfile(module_file):
            return self

        modules = gitconfig.module_read(git_directory=self.pathname)

        for module_name, module_url in modules.items():
            # check if module is already added to remote
            # encode name to base64 to ensure naming compatiblity in .git/config
            module_b64name = '__submodule__' \
                            + base64.standard_b64encode(module_name.encode()).decode()

            remote_url = gitconfig.remote_read(git_directory=self.pathname,
                                               name=module_b64name)

            # check if an update is required
            if not isinstance(remote_url, dict) \
            or not isinstance(remote_url.get(module_b64name), str):
                # default behavior. Add.
                pass
            elif remote_url[module_b64name] == module_url:
                # nothing needs to be done
                continue
            else:
                # remote_url in .git/config does not match
                # remove original before (re-)Add.
                self.del_remote(module_b64name)

            # add module_name and url to .git./config
            self.add_remote(module_b64name, module_url)
        return self

    def make_buildrepo(self):
        """Workflow to create or update the buildrepo, consists of two steps:
        1. clone or pull main repository,
        2. read .gitmodules and merge repositories into main."""
        self.pullmain()
        self.merge_submodules(remove_existing=True)
        return self
