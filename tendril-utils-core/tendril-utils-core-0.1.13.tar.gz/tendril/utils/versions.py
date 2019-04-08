#!/usr/bin/env python
# encoding: utf-8

# Copyright (C) 2016-2019 Chintalagiri Shashank
#
# This file is part of tendril.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from __future__ import print_function
import pkg_resources


def get_version(package):
    try:
        return pkg_resources.get_distribution(package).version
    except pkg_resources.DistributionNotFound:
        return 'Not Installed'


def get_versions(prefix):
    return sorted([(d.project_name, d.version)
                   for d in pkg_resources.working_set
                   if d.project_name.startswith(prefix)],
                  key=lambda x: x[0])


class FeatureUnavailable(Exception):
    def __init__(self, feature=None, provider=None):
        self._feature = feature
        self._provider = provider

    def __repr__(self):
        return "<FeatureUnavailable {0}>\nThis feature might be provided by " \
               "{1}.".format(self._feature, self._provider)


def main():
    print(' {0:34} : {1}'.format('Tendril Version',
                                 get_version('tendril-framework')))
    print(' Installed Components : ')
    for package, version in get_versions('tendril'):
        print('   {0:32} : {1}'.format(package, version))


if __name__ == '__main__':
    main()
