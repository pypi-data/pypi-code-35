# Copyright 2015 Planet Labs, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

import datetime
import os
import pytest
import random
import six
import string
import uuid


try:
    from moto import mock_s3
    import boto.s3
    from boto.s3.key import Key
    from six.moves.urllib.parse import urlparse
    import simplejson as json
except ImportError:
    # if developers use s3-test features without having installed s3 stuff,
    # things will fail. So it goes.
    pass


@pytest.fixture
def basic_metadata():

    return {
        'version': 1,
        'start': '2018-05-23T00:00:00Z',
        'end': '2018-05-24T01:20:30Z',
        'path': '/var/log/apache/access.log',
        'where': 'nebraska',
        'what': 'apache',
        'cid': '12345',
        'work_id': None,
    }


def random_word(length):
    if six.PY2:
        lowercase = string.lowercase
    else:
        lowercase = string.ascii_lowercase
    return ''.join(random.choice(lowercase) for i in range(length))


def random_hex(length):
    return ('%0' + str(length) + 'x') % random.randrange(16**length)


def random_interval():
    year_2010 = 1262304000
    five_years = 5 * 365 * 24 * 60 * 60
    three_days = 3 * 24 * 60 * 60
    start = year_2010 + random.randint(0, five_years)
    end = start + random.randint(0, three_days)
    start = datetime.datetime.utcfromtimestamp(start)
    start = start.isoformat('T', 'milliseconds')
    end = datetime.datetime.utcfromtimestamp(end)
    end = end.isoformat('T', 'milliseconds')
    return start, end


def random_work_id():
    if random.randint(0, 1):
        return None
    return '{}-{}'.format(random_word(5), random.randint(0, 2**15))


def random_abs_dir():
    num_dirs = random.randrange(1, 4)
    lengths = [random.randint(2, 10) for i in range(num_dirs)]
    dirs = [random_word(i) for i in lengths]
    return '/' + '/'.join(dirs)


@pytest.fixture
def random_metadata():
    start, end = random_interval()
    what = random_word(10)
    return {
        'version': 1,
        'start': start,
        'end': end,
        'path': os.path.join(random_abs_dir(), what),
        'work_id': random_work_id(),
        'where': random_word(10),
        'what': what,
        'uuid': str(uuid.uuid4()),
        'cid': random_hex(32),
    }


@pytest.fixture
def tmpfile(tmpdir):
    name = random_word(10)

    def get_tmpfile(content):
        f = tmpdir.join(name)
        f.write(content)
        return str(f)

    return get_tmpfile


@pytest.fixture
def aws_connector(request):

    def create_connection(mocker, connector):
        mock = mocker()
        mock.start()

        def tear_down():
            mock.stop()
        request.addfinalizer(tear_down)

        return connector()

    return create_connection


@pytest.fixture
def s3_connection(aws_connector):
    return aws_connector(mock_s3, boto.connect_s3)


@pytest.fixture
def s3_bucket_maker(s3_connection):

    def maker(bucket_name):
        return s3_connection.create_bucket(bucket_name)

    return maker


@pytest.fixture
def s3_file_maker(s3_bucket_maker):

    def maker(bucket, key, content, metadata):
        b = s3_bucket_maker(bucket)
        k = Key(b)
        k.key = key
        if metadata:
            k.set_metadata('datalake', json.dumps(metadata))
        k.set_contents_from_string(content)

    return maker


@pytest.fixture
def s3_file_from_metadata(s3_file_maker):

    def maker(url, metadata):
        url = urlparse(url)
        assert url.scheme == 's3'
        s3_file_maker(url.netloc, url.path, '', metadata)

    return maker
