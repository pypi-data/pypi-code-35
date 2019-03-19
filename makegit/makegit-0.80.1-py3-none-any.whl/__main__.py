#!/usr/bin/env python3
"""
Copyright (c) 2019 LINKIT, The Netherlands. All Rights Reserved.
Author(s): Anthony Potappel

This software may be modified and distributed under the terms of the
MIT license. See the LICENSE file for details.
"""

import os
import sys
import argparse

from .main.makegit import MakeGit

def main():
    """This function is called when run as python3 -m ${MODULE}
    Parse any additional arguments and call required module functions."""

    module_name = '.'.join(__loader__.name.split('.')[0:-1])

    argument_parser = argparse.ArgumentParser(
        prog=module_name,
        description='Merge GIT submodule repositories into a single buildrepo'
    )

    # Makefile: make git url=$GIT_URL}
    argument_parser.add_argument('--url', action='store', nargs=1, required=True,
                                 help='URL of originating buildplan repository')
    argument_parser.add_argument('--build_directory', action='store', nargs=1, required=False,
                                 default=['build'],
                                 help='BUILD_DIRECTORY used to store merged repository, \
                                       Defaults to "build"')
    argument_parser.add_argument('--buildrepo_linkname', action='store', nargs=1, required=False,
                                 default=['buildrepo'],
                                 help='BUILDREPO_LINKNAME is the name of the symlink pointing \
                                       to active repository. Defaults to "buildrepo"')

    args = argument_parser.parse_args(sys.argv[1:])

    build_directory = args.build_directory[0]
    buildrepo_linkname = build_directory + '/' + args.buildrepo_linkname[0]

    repository = MakeGit(giturl=args.url[0],
                         build_directory=build_directory,
                         verbose=True)
    repository.make_buildrepo()

    if os.path.islink(buildrepo_linkname) is True:
        os.unlink(buildrepo_linkname)
    elif os.path.exists(buildrepo_linkname) is True:
        # a file exists that is not a symlink
        print('File exist, cant create symlink: ' + buildrepo_linkname)
        sys.exit(1)
    os.symlink(repository.reponame, buildrepo_linkname)

    return 0


if __name__ == '__main__':
    sys.exit(main())
