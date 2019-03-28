import unittest

import os
import pathlib
import json

setup_path = pathlib.Path(os.path.dirname(os.path.relpath(__file__)))

from rc_cli.client import *
from ..assignment_seeder.assignment_seeder import AssignmentSeeder
from rc_cli.gitlab.groups_api import GroupsApi
from rc_cli.gitlab.projects_api import ProjectsApi
from rc_cli.gitlab.users_api import UsersApi

from unittest.mock import MagicMock
from unittest.mock import patch

import requests
import click
from click.testing import CliRunner

class AssignmentSeederTests(unittest.TestCase):

    @patch(__name__ + '.AssignmentSeeder._verbose')
    @patch(__name__ + '.AssignmentSeeder._error')
    def test_get_students_names(self, error, verbose):
        student_name_path = "./names.txt"
        runner = CliRunner()
        with runner.isolated_filesystem():
            f = open(student_name_path, 'w')
            f.write("member1\nmember2")
            f.close()
            seeder = AssignmentSeeder(None, "class", "assignment", student_name_path,
                                      "token", True, False)
            names = seeder.get_student_names(student_name_path)
            self.assertEqual(len(names), 2)
            self.assertEqual(names[0], "member1\n")
            self.assertEqual(names[1], "member2")

    @patch(__name__ + '.AssignmentSeeder._verbose')
    @patch(__name__ + '.AssignmentSeeder._error')
    def test_get_students_names_no_names(self, error, verbose):
        student_name_path = "./names.txt"
        runner = CliRunner()
        with runner.isolated_filesystem():
            f = open(student_name_path, 'w')
            f.close()
            seeder = AssignmentSeeder(None, "class", "assignment", student_name_path,
                                      "token", True, False)
            names = seeder.get_student_names(student_name_path)
            self.assertEqual(len(names), 0)

    @patch(__name__ + '.AssignmentSeeder._verbose')
    @patch(__name__ + '.AssignmentSeeder._error')
    def test_get_teams(self, error, verbose):
        student_name_path = "./names.txt"
        runner = CliRunner()
        with runner.isolated_filesystem():
            f = open(student_name_path, 'w')
            f.write("team1,member1,member2\nteam2,member3")
            f.close()
            seeder = AssignmentSeeder(None, "class", "assignment", student_name_path,
                                      "token", True, False)
            names = seeder.get_team_sets(student_name_path)
            self.assertEqual(len(names), 2)
            self.assertEqual(names["team1"][0], "member1")
            self.assertEqual(names["team1"][1], "member2")
            self.assertEqual(names["team2"][0], "member3")

    @patch(__name__ + '.AssignmentSeeder._verbose')
    @patch(__name__ + '.AssignmentSeeder._error')
    def test_get_teams_no_names(self, error, verbose):
        student_name_path = "./names.txt"
        runner = CliRunner()
        with runner.isolated_filesystem():
            f = open(student_name_path, 'w')
            f.close()
            seeder = AssignmentSeeder(None, "class", "assignment", student_name_path,
                                      "token", True, False)
            names = seeder.get_team_sets(student_name_path)
            self.assertEqual(len(names), 0)

    @patch(__name__ + '.AssignmentSeeder._verbose')
    @patch(__name__ + '.AssignmentSeeder._warn')
    @patch(__name__ + '.GroupsApi.search_groups')
    def test_create_class_group_exists(self, search_groups, warn, verbose):
        student_name_path = "./names.txt"
        runner = CliRunner()
        project_id = 1111
        search_results = [
            {
                "id": project_id
            }
        ]
        search_groups.return_value = (search_results, 200)

        with runner.isolated_filesystem():
            f = open(student_name_path, 'w')
            f.close()
            seeder = AssignmentSeeder(None, "class", "assignment", student_name_path,
                                      "token", True, False)
            id = seeder.create_class_group()
            self.assertEqual(id, project_id)
            warn.assert_called()

    @patch(__name__ + '.AssignmentSeeder._verbose')
    @patch(__name__ + '.AssignmentSeeder._error')
    @patch(__name__ + '.GroupsApi.search_groups')
    @patch(__name__ + '.GroupsApi.create_group')
    def test_create_class_group_new_project(self, create_group, search_groups, error, verbose):
        student_name_path = "./names.txt"
        runner = CliRunner()
        project_id = 1111
        search_results = []
        create_results = {
                "id": project_id
            }

        search_groups.return_value = (search_results, 202)
        create_group.return_value = (create_results, 202)

        with runner.isolated_filesystem():
            f = open(student_name_path, 'w')
            f.close()
            seeder = AssignmentSeeder(None, "class", "assignment", student_name_path,
                                      "token", True, False)
            id = seeder.create_class_group()
            self.assertEqual(id, "")
            error.assert_called()

    @patch(__name__ + '.AssignmentSeeder._verbose')
    @patch(__name__ + '.AssignmentSeeder._error')
    @patch(__name__ + '.GroupsApi.search_groups')
    @patch(__name__ + '.GroupsApi.create_group')
    def test_create_class_group_new_project_fail_create(self, create_group, search_groups, error, verbose):
        student_name_path = "./names.txt"
        runner = CliRunner()
        search_results = []
        create_results = {}

        search_groups.return_value = (search_results, 202)
        create_group.return_value = (create_results, 202)

        with runner.isolated_filesystem():
            f = open(student_name_path, 'w')
            f.close()
            seeder = AssignmentSeeder(None, "class", "assignment", student_name_path,
                                      "token", True, False)
            id = seeder.create_class_group()
            self.assertEqual(id, '')
            error.assert_called()

    @patch(__name__ + '.AssignmentSeeder._verbose')
    @patch(__name__ + '.AssignmentSeeder._error')
    @patch(__name__ + '.ProjectsApi.get_namespace')
    @patch(__name__ + '.GroupsApi.create_group')
    def test_create_assignment_group(self, create_group, get_namespace, error, verbose):
        student_name_path = "./names.txt"
        group_id = 1111
        runner = CliRunner()
        namespace = "namespace"
        create_results = {
            "id": group_id
        }

        get_namespace.return_value = namespace
        create_group.return_value = (create_results, 202)

        with runner.isolated_filesystem():
            f = open(student_name_path, 'w')
            f.close()
            seeder = AssignmentSeeder(None, "class", "assignment", student_name_path,
                                      "token", True, False)
            (id, name) = seeder.create_assignment_group("", 1111)
            self.assertEqual(id, group_id)
            self.assertEqual(name, namespace)

    @patch(__name__ + '.AssignmentSeeder._verbose')
    @patch(__name__ + '.AssignmentSeeder._error')
    @patch(__name__ + '.ProjectsApi.search_project')
    @patch(__name__ + '.ProjectsApi.create_project')
    def test_create_all_repo(self, create_project, search_project, error, verbose):
        student_name_path = "./names.txt"
        web_url = "url"
        group_id = 1111
        runner = CliRunner()
        create_results = {
            "id": group_id,
            "web_url": "url"
        }

        search_project.return_value = ({},202)
        create_project.return_value = (create_results, 202)

        with runner.isolated_filesystem():
            f = open(student_name_path, 'w')
            f.close()
            seeder = AssignmentSeeder(None, "class", "assignment", student_name_path,
                                      "token", True, False)
            (id, web) = seeder.create_all_repo("", 1111, "")
            self.assertEqual(id, group_id)
            self.assertEqual(web, web_url + ".git")

    @patch(__name__ + '.AssignmentSeeder._verbose')
    @patch(__name__ + '.AssignmentSeeder._warn')
    @patch(__name__ + '.ProjectsApi.search_project')
    @patch(__name__ + '.ProjectsApi.create_project')
    def test_create_student_repo_exists(self, create_project, search_project, warn, verbose):
        student_name_path = "./names.txt"
        project_name = "name"
        owner_id = 19
        seed_repo_url = "url"
        namespace = "namespace"
        student = "student"
        runner = CliRunner()
        data = ["repo"]

        search_project.return_value = (data,202)

        with runner.isolated_filesystem():
            f = open(student_name_path, 'w')
            f.close()
            seeder = AssignmentSeeder(None, "class", "assignment", student_name_path,
                                      "token", True, False)
            seeder.create_student_repo(project_name, owner_id,
                                       seed_repo_url, namespace,
                                       student)
            warn.assert_called()
            create_project.assert_not_called()

    @patch(__name__ + '.AssignmentSeeder._verbose')
    @patch(__name__ + '.AssignmentSeeder._success')
    @patch(__name__ + '.ProjectsApi.search_project')
    @patch(__name__ + '.ProjectsApi.create_project')
    @patch(__name__ + '.ProjectsApi.unprotect_branch')
    @patch(__name__ + '.AssignmentSeeder.add_member')
    def test_create_student_repo_not_exists(self, add_member, unprotect_branch, create_project, search_project, success, verbose):
        student_name_path = "./names.txt"
        project_name = "name"
        owner_id = "19"
        seed_repo_url = "url"
        namespace = "namespace"
        student = "student"
        runner = CliRunner()
        data = []

        project_return = {
            "id": "id",
            "web_url": "url",
            "path": "path"
        }

        search_project.return_value = (data,202)
        create_project.return_value = (project_return, 202)

        with runner.isolated_filesystem():
            f = open(student_name_path, 'w')
            f.close()
            seeder = AssignmentSeeder(None, "class", "assignment", student_name_path,
                                      "token", True, False)
            seeder.create_student_repo(project_name, owner_id,
                                       seed_repo_url, namespace,
                                       student)
            success.assert_called()
            create_project.assert_called()
            add_member.assert_called()
            unprotect_branch.assert_called()


    @patch(__name__ + '.UsersApi.search_user_by_username')
    @patch(__name__ + '.ProjectsApi.add_member')
    def test_add_members_no_teamsets(self, add_member, search_user_by_username):
        student_name_path = "./names.txt"
        pID = "id"
        student = "student"
        runner = CliRunner()
        data = [{
            "id": "id"
        }]

        search_user_by_username.return_value = (data,202)

        with runner.isolated_filesystem():
            f = open(student_name_path, 'w')
            f.close()
            seeder = AssignmentSeeder(None, "class", "assignment", student_name_path,
                                      "token", True, False)
            seeder.add_member(student, pID)
            add_member.assert_called()
            search_user_by_username.assert_called()

    @patch(__name__ + '.UsersApi.search_user_by_username')
    @patch(__name__ + '.ProjectsApi.add_member')
    def test_add_members_teamsets(self, add_member, search_user_by_username):
        student_name_path = "./names.txt"
        pID = "id"
        student = ["student","student2"]
        runner = CliRunner()
        data = [{
            "id": "id"
        }]

        search_user_by_username.return_value = (data,202)

        with runner.isolated_filesystem():
            f = open(student_name_path, 'w')
            f.close()
            seeder = AssignmentSeeder(None, "class", "assignment", student_name_path,
                                      "token", True, True)
            seeder.add_member(student, pID)
            add_member.assert_called()
            search_user_by_username.assert_called()
            self.assertEqual(search_user_by_username.call_count,2)