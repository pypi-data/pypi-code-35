import click
import json
import unittest
import requests
from git import GitCommandError
from rc_cli.init import initializer
from unittest.mock import MagicMock, patch
from ..gitlab.groups_api import GroupsApi


class InitializerTests(unittest.TestCase):

    def setUp(self):
        self.initializer_directory = './initializerDirectory'
        self.config = ''
        self.click_prompt = click.prompt
        self.click_style = click.style
        self.click_open_file = click.open_file
        self.json_dumps = json.dumps
        self.requests_codes = requests.codes

        click.prompt = MagicMock(return_value='token')
        requests.codes = MagicMock()
        requests.codes.ok = 'ok'

    def tearDown(self):
        click.prompt = self.click_prompt
        click.style = self.click_style
        click.open_file = self.click_open_file
        json.dumps = self.json_dumps
        requests.codes = self.requests_codes

    def create_initializer(self, url):
        init = initializer.Initializer(self.config,
                                       self.initializer_directory,
                                       url)
        init.config = 'config'
        init._verbose = MagicMock()
        init._error = MagicMock()
        init._warn = MagicMock()
        init._success = MagicMock()
        return init

    def test_execute_workspace_json_are_created(self):
        init = self.create_initializer('')
        init._Initializer__create_workspace = MagicMock(return_value=True)
        init._Initializer__create_config_json = MagicMock(return_value=True)

        with self.assertRaises(SystemExit) as cm:
            init.execute()

        self.assertEqual(cm.exception.code, 0)
        self.assertEqual(init._success.call_count, 2)
        self.assertEqual(init._verbose.call_count, 2)

    def test_execute_json_is_not_created(self):
        init = self.create_initializer('')
        init._Initializer__create_workspace = MagicMock(return_value=True)
        init._Initializer__create_config_json = MagicMock(return_value=False)

        with self.assertRaises(SystemExit) as cm:
            init.execute()

        self.assertEqual(cm.exception.code, 1)
        self.assertEqual(init._success.call_count, 0)
        self.assertEqual(init._verbose.call_count, 2)

    def test_execute_workspace_is_not_created(self):
        init = self.create_initializer('')
        init._Initializer__create_workspace = MagicMock(return_value=False)
        init._Initializer__create_config_json = MagicMock(return_value=True)

        with self.assertRaises(SystemExit) as cm:
            init.execute()

        self.assertEqual(cm.exception.code, 1)
        self.assertEqual(init._success.call_count, 0)
        self.assertEqual(init._verbose.call_count, 1)

    def test_create_workspace_success(self):
        init = self.create_initializer('')
        init.base = MagicMock(returnValue=None)

        self.assertEqual(init._Initializer__create_workspace(), True)

    def test_create_workspace_failure(self):
        init = self.create_initializer('')
        init.base = MagicMock(return_value=None)
        init.base.mkdir.side_effect = FileExistsError

        self.assertEqual(init._Initializer__create_workspace(), False)

    def test_create_config_already_exists(self):
        init = self.create_initializer('')
        config_path_mock = MagicMock()
        config_path_mock.exists = MagicMock(return_value=True)
        init.config_path = MagicMock(return_value=config_path_mock)
        init._validate = MagicMock(return_value=None)

        self.assertEqual(init._Initializer__create_config_json(), False)
        self.assertEqual(init._validate.call_count, 1)

    def test_create_config_does_not_exist_url_is_none(self):
        init = self.create_initializer(None)
        config_path_mock = MagicMock()
        config_path_mock.exists = MagicMock(return_value=False)
        init.config_path = MagicMock(return_value=config_path_mock)
        init._Initializer__handle_new_workspace = MagicMock(
            return_value="config")

        click.open_file = MagicMock()
        click.open_file.__enter__.write = MagicMock()
        json.dumps = MagicMock(return_value='json config')

        self.assertEqual(init._Initializer__create_config_json(), True)

        self.assertEqual(init._verbose.call_count, 1)
        self.assertEqual(
            click.open_file.return_value.__enter__.return_value.write.call_args,
            (('json config',),))


    def test_create_config_does_not_exist_url_exists(self):
        init = self.create_initializer('url')
        config_path_mock = MagicMock()
        config_path_mock.exists = MagicMock(return_value=False)
        init.config_path = MagicMock(return_value=config_path_mock)
        init._Initializer__handle_from_url = MagicMock(return_value="config")

        click.open_file = MagicMock()
        json.dumps = MagicMock(return_value='json config')

        self.assertEqual(init._Initializer__create_config_json(), True)

        self.assertEqual(init._verbose.call_count, 1)
        self.assertEqual(
            click.open_file.return_value.__enter__.return_value.write.call_args,
            (('json config',),))


    def test_handle_new_workspace(self):
        self.maxDiff = None
        init = self.create_initializer(None)
        init._Initializer__get_default_lfs = MagicMock(return_value='lfs')

        click.style = MagicMock(return_value='')

        def prompt_mock(style, type, default='', show_default=None):
            return default

        click.prompt.side_effect = prompt_mock

        default_workspaces = [
            {
                'name': 'assignments',
                'description': '',
                'path': '',
                'visibility': 'private',
                'lfs_enabled': False,
                'request_access_enabled': False
            },
            {
                'name': 'exams',
                'description': '',
                'path': '',
                'visibility': 'private',
                'lfs_enabled': False,
                'request_access_enabled': False
            }
        ]
        default_resources = {
            'name': 'content',
            'description': '',
            'path': '',
            'visibility': 'private',
            'lfs_enabled': True,
            'request_access_enabled': False
        }

        example = {
            'gitlab': {
                'url': 'https://ada.csse.rose-hulman.edu',
                'token': '',
                'group': {
                    'name': '',
                    'description': '',
                    'visibility': 'private',
                    'lfs_enabled': False,
                    'request_access_enabled': True,
                    'parent_id': ''
                }
            },
            'workspaces': default_workspaces,
            'resources': default_resources,
            'lfs': 'lfs'
        }

        self.assertEqual(init._Initializer__handle_new_workspace(), example)

    def test_handle_from_url_empty_token(self):
        init = self.create_initializer(None)
        click.prompt = MagicMock(return_value='')
        click.style = MagicMock(return_value='')

        with self.assertRaises(SystemExit) as cm:
            init._Initializer__handle_from_url()

        self.assertEqual(cm.exception.code, 1)
        self.assertEqual(init._error.call_count, 1)
        self.assertEqual(init._warn.call_count, 1)

    @patch(__name__ + '.GroupsApi.search_groups')
    def test_get_parent_group_bad_status(self, search_groups):
        init = self.create_initializer(None)

        urlparse = MagicMock(return_value='url')
        urlunsplit = MagicMock()
        urlunsplit.return_value.path = [['group']]
        urljoin = MagicMock(return_value='url/api/v4/')

        def subgroup_get(item):
            return 'subgroup' + item

        search_groups.return_value = (None, 'not ok')

        with self.assertRaises(SystemExit) as cm:
            init._Initializer__handle_from_url()

        self.assertEqual(init._error.call_count, 1)

    @patch(__name__ + '.GroupsApi.search_groups')
    def test_get_parent_group_bad_parent_group(self, search_groups):
        init = self.create_initializer(None)
        requests.codes = MagicMock()
        requests.codes.return_value.ok = 'ok'

        urlparse = MagicMock(return_value='url')
        urlunsplit = MagicMock()
        urlunsplit.return_value.path = [['group']]
        urljoin = MagicMock(return_value='url/api/v4/')

        def subgroup_get(item):
            return 'subgroup' + item

        search_groups.return_value = (None, 'ok')

        with self.assertRaises(SystemExit) as cm:
            init._Initializer__handle_from_url()

        self.assertEqual(init._error.call_count, 1)

    @patch(__name__ + '.GroupsApi.search_groups')
    @patch(__name__ + '.GroupsApi.get_subgroups')
    def test_get_subgroups_bad_status(self, search_groups, get_subgroups):
        init = self.create_initializer(None)

        urlparse = MagicMock(return_value='url')
        urlunsplit = MagicMock()
        urlunsplit.return_value.path = [['group']]
        urljoin = MagicMock(return_value='url/api/v4/')

        def subgroup_get(item):
            return 'subgroup' + item

        group_mock = MagicMock()
        group_mock.get.return_value = 'group'
        search_groups.return_value = ([group_mock], 'ok')
        get_subgroups.return_value = (None, 'not ok')

        with self.assertRaises(SystemExit) as cm:
            init._Initializer__handle_from_url()

        self.assertEqual(init._error.call_count, 1)

    @patch(__name__ + '.GroupsApi.search_groups')
    @patch(__name__ + '.GroupsApi.get_subgroups')
    @patch(__name__ + '.GroupsApi.get_group_projects')
    def test_get_group_projects_bad_status(self,
                                           get_group_projects,
                                           get_subgroups,
                                           search_groups):

        init = self.create_initializer(None)

        urlparse = MagicMock(return_value='url')
        urlunsplit = MagicMock()
        urlunsplit.return_value.path = [['group']]
        urljoin = MagicMock(return_value='url/api/v4/')

        def subgroup_get(item):
            return 'subgroup' + item

        group_mock = MagicMock()
        group_mock.get.return_value = 'group'
        search_groups.return_value = ([group_mock], 'not ok')
        get_subgroups.return_value = (None, 'ok')
        get_group_projects.return_value = (None, 'not ok')

        with self.assertRaises(SystemExit) as cm:
            init._Initializer__handle_from_url()

        self.assertEqual(init._error.call_count, 1)

    @patch(__name__ + '.GroupsApi.search_groups')
    @patch(__name__ + '.GroupsApi.get_subgroups')
    @patch(__name__ + '.GroupsApi.get_group_projects')
    def test_get_group_projects_bad_repos(self,
                                          get_group_projects,
                                          get_subgroups,
                                          search_groups):

        init = self.create_initializer(None)

        urlparse = MagicMock(return_value='url')
        urlunsplit = MagicMock()
        urlunsplit.return_value.path = [['group']]
        urljoin = MagicMock(return_value='url/api/v4/')

        group_mock = MagicMock()
        group_mock.get.return_value = 'group'
        search_groups.return_value = ([group_mock], 'ok')
        get_subgroups.return_value = (None, 'ok')
        get_group_projects.return_value = (['item1', 'item2'], 'ok')

        with self.assertRaises(SystemExit) as cm:
            init._Initializer__handle_from_url()

        self.assertEqual(init._error.call_count, 1)

    @patch('git.Repo')
    @patch(__name__ + '.GroupsApi.search_groups')
    @patch(__name__ + '.GroupsApi.get_subgroups')
    @patch(__name__ + '.GroupsApi.get_group_projects')
    def test_get_resources_repo_too_many(self,
                                         get_group_projects,
                                         get_subgroups,
                                         search_groups,
                                         repo):

        init = self.create_initializer(None)
        init.base = MagicMock()

        urlparse = MagicMock()
        urlparse.return_value.path = ['h', 'group']
        urlunsplit = MagicMock()
        urlunsplit.return_value.path = [['group']]
        urljoin = MagicMock(return_value='url/api/v4/')

        group_mock = MagicMock()
        group_mock.get.return_value = b''
        search_groups.return_value = ([group_mock], 'ok')
        subgroup_mock1 = MagicMock()
        subgroup_mock1.get.return_value = 'subgroup'
        subgroup_mock2 = MagicMock()
        subgroup_mock2.get.return_value = 'subgroup2'
        subgroup_mock3 = MagicMock()
        subgroup_mock3.get.return_value = 'subgroup3'
        get_subgroups.return_value = (
        [subgroup_mock1, subgroup_mock2, subgroup_mock3], 'ok')
        get_group_projects.return_value = (['item1', 'item2'], 'ok')

        path_mock = MagicMock()
        path_mock.mkdir.side_effect = FileExistsError

        path_mock2 = MagicMock()
        path_mock3 = MagicMock()
        path_mock4 = MagicMock()

        def joinpath_side_effect(name):
            if name == 'subgroup':
                return path_mock
            if name == 'subgroup2':
                return path_mock2
            if name == 'subgroup3':
                return path_mock3
            if name == 'url':
                return path_mock4

        init.base.joinpath.side_effect = joinpath_side_effect

        repo_mock = MagicMock()
        repo_mock.get.return_value = 'repo'
        project_mock = MagicMock()
        project_mock.get.return_value = 'url'

        def get_group_projects_side_effects(idIn, headers):
            if idIn == 'subgroup1' or idIn == 'subgroup2':
                return None, 'not ok'
            if idIn == 'subgroup3':
                return [project_mock], 'ok'
            return [(repo_mock, 'junk')], 'ok'

        get_group_projects.side_effects = get_group_projects_side_effects

        repo.clone_from.side_effect = GitCommandError

        with self.assertRaises(SystemExit):
            init._Initializer__handle_from_url()

        self.assertEqual(init._error.call_count, 1)
        self.assertEqual(init._error.call_args, (
        ('Expected one resources repository per group but got 2',),))

    @patch(__name__ + '.GroupsApi.search_groups')
    @patch(__name__ + '.GroupsApi.get_subgroups')
    @patch(__name__ + '.GroupsApi.get_group_projects')
    def test_handle_from_url_success(self,
                                     get_group_projects,
                                     get_subgroups,
                                     search_groups):
        self.maxDiff = None
        init = self.create_initializer(None)
        init.base = MagicMock()
        init._Initializer__get_default_lfs = MagicMock(return_value='lfs')

        urlparse = MagicMock()
        urlparse.return_value.path = ['h', 'group']
        urlunsplit = MagicMock()
        urlunsplit.return_value.path = [['group']]
        urljoin = MagicMock(return_value='url/api/v4/')

        group_mock = MagicMock()
        group_mock.get.return_value = b''
        search_groups.return_value = ([group_mock], 'ok')
        subgroup_mock1 = MagicMock()
        subgroup_mock1.get.return_value = 'subgroup'
        subgroup_mock2 = MagicMock()
        subgroup_mock2.get.return_value = 'subgroup2'
        subgroup_mock3 = MagicMock()
        subgroup_mock3.get.return_value = 'subgroup3'
        get_subgroups.return_value = (
        [subgroup_mock1, subgroup_mock2, subgroup_mock3], 'ok')
        repo_mock = MagicMock()
        repo_mock.get.return_value = 'repo'
        get_group_projects.return_value = ([repo_mock], 'ok')

        path_mock = MagicMock()
        path_mock.mkdir.side_effect = FileExistsError

        path_mock2 = MagicMock()
        path_mock3 = MagicMock()
        path_mock4 = MagicMock()

        def joinpath_side_effect(name):
            if name == 'subgroup':
                return path_mock
            if name == 'subgroup2':
                return path_mock2
            if name == 'subgroup3':
                return path_mock3
            if name == 'url':
                return path_mock4

        init.base.joinpath.side_effect = joinpath_side_effect

        repo_mock = MagicMock()
        repo_mock.get.return_value = 'repo'
        project_mock = MagicMock()
        project_mock.get.return_value = 'url'

        def get_group_projects_side_effects(idIn, headers):
            if idIn == 'subgroup1' or idIn == 'subgroup2':
                return None, 'not ok'
            if idIn == 'subgroup3':
                return [project_mock], 'ok'
            return [(repo_mock, 'junk')], 'ok'

        get_group_projects.side_effects = get_group_projects_side_effects

        example = {
            'gitlab': {
                'url': b'',
                'token': 'token',
                'group': {
                    'name': b'',
                    'description': b'',
                    'visibility': b'',
                    'lfs_enabled': b'',
                    'request_access_enabled': b'',
                    'parent_id': b''
                }
            },
            'workspaces': [{
                'name': 'subgroup',
                'description': 'subgroup',
                'path': '',
                'visibility': 'subgroup',
                'lfs_enabled': 'subgroup',
                'request_access_enabled': 'subgroup'
            },
                {
                    'name': 'subgroup2',
                    'description': 'subgroup2',
                    'path': '',
                    'visibility': 'subgroup2',
                    'lfs_enabled': 'subgroup2',
                    'request_access_enabled': 'subgroup2'
                },
                {
                    'name': 'subgroup3',
                    'description': 'subgroup3',
                    'path': '',
                    'visibility': 'subgroup3',
                    'lfs_enabled': 'subgroup3',
                    'request_access_enabled': 'subgroup3'
                }],
            'resources': {
                'name': 'repo',
                'description': 'repo',
                'path': '',
                'visibility': 'repo',
                'lfs_enabled': 'repo',
                'request_access_enabled': 'repo'
            },
            'lfs': 'lfs'
        }
        self.assertEquals(init._Initializer__handle_from_url(), example)
