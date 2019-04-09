# Copyright (C) 2019  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

import json
import os
import os.path

RESOURCES_PATH = os.path.join(os.path.dirname(__file__), 'resources')

package = 'org'
package_url = 'https://www.npmjs.com/package/%s' % package
package_metadata_url = 'https://replicate.npmjs.com/%s/' % package

FIRST_VISIT_PACKAGE_METADATA_JSON_FILENAME = 'org_metadata_visit1.json'
SECOND_VISIT_PACKAGE_METADATA_JSON_FILENAME = 'org_metadata_visit2.json'


class _MockedFileStream():
    def __init__(self, file_data):
        self.file_data = file_data
        self.closed = False

    def read(self):
        self.closed = True
        return self.file_data


def init_test_data(m, package_metadata_json_file):

    org_metadata_filepath = os.path.join(RESOURCES_PATH,
                                         package_metadata_json_file)

    with open(org_metadata_filepath) as json_file:
        package_metadata = json.load(json_file)

    m.register_uri('GET', package_metadata_url, json=package_metadata)

    for v, v_data in package_metadata['versions'].items():
        tarball_url = v_data['dist']['tarball']
        tarball_filename = tarball_url.split('/')[-1]
        tarball_filepath = os.path.join(RESOURCES_PATH, 'tarballs',
                                        tarball_filename)
        with open(tarball_filepath, mode='rb') as tarball_file:
            tarball_content = tarball_file.read()
            m.register_uri('GET', tarball_url,
                           body=_MockedFileStream(tarball_content))

    return package_metadata


def get_package_versions_data(package_metadata):
    versions_data = {}
    for v, v_data in package_metadata['versions'].items():
        shasum = v_data['dist']['shasum']
        versions_data[(v, shasum)] = {
            'name': package,
            'version': v,
            'sha1': shasum,
            'url': v_data['dist']['tarball'],
            'filename': v_data['dist']['tarball'].split('/')[-1],
            'date': package_metadata['time'][v]
        }
    return versions_data
