
import pytest
import responses

import datarobot as dr
from tests.utils import request_body_to_json


class TestHDFSCreate(object):
    @pytest.fixture
    def hdfs_create_response(self, unittest_endpoint, async_url):
        mysql_create_url = '{}/{}/'.format(unittest_endpoint, 'hdfsProjects')
        responses.add(
            responses.POST,
            mysql_create_url,
            body='',
            status=202,
            content_type='application/json',
            adding_headers={'Location': async_url}
        )

    @responses.activate
    @pytest.mark.usefixtures('client',
                             'project_creation_responses',
                             'hdfs_create_response')
    def test_create_hdfs_minimum(self):
        dr.Project.create_from_hdfs(url='hdfs://webhdfs.com/directory/file.csv')
        create_body = request_body_to_json(responses.calls[0].request)
        assert create_body['url'] == 'hdfs://webhdfs.com/directory/file.csv'

    @responses.activate
    @pytest.mark.usefixtures('client',
                             'project_creation_responses',
                             'hdfs_create_response')
    def test_create_hdfs_all_options(self):
        dr.Project.create_from_hdfs(url='hdfs://webhdfs.com/directory/file.csv',
                                    port=9999,
                                    project_name='HDFS Project',
                                    max_wait=100)
        create_body = request_body_to_json(responses.calls[0].request)
        assert create_body['url'] == 'hdfs://webhdfs.com/directory/file.csv'
        assert create_body['port'] == 9999
        assert create_body['projectName'] == 'HDFS Project'


class TestDataSourceCreate(object):
    @pytest.fixture
    def data_source_create_response(self, unittest_endpoint, async_url):
        project_create_url = '{}/{}'.format(unittest_endpoint, dr.Project._path)
        responses.add(
            responses.POST,
            project_create_url,
            body='',
            status=202,
            content_type='application/json',
            adding_headers={'Location': async_url}
        )

    @pytest.fixture
    def data_source(self):
        return dr.DataSource('5acc8437ec8d670001ba16bf')

    @responses.activate
    @pytest.mark.usefixtures('client',
                             'project_creation_responses',
                             'data_source_create_response')
    def test_create_from_data_source_id(self):
        username = 'test_user'
        password = 'megasuperubersecretpassword'
        data_source_id = '5acc8437ec8d670001ba16bf'
        project_name = 'data source project'
        dr.Project.create_from_data_source(data_source_id, username, password,
                                           project_name=project_name)
        create_body = request_body_to_json(responses.calls[0].request)
        assert create_body == {
            'user': username,
            'password': password,
            'dataSourceId': data_source_id,
            'projectName': project_name
        }
