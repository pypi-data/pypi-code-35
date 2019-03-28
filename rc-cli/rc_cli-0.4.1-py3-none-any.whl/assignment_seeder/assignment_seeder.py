"""This file will create all repos needed for an assignment"""
import time
import os
import shutil
import json
import stat

from datetime import date
from datetime import datetime
from datetime import timedelta
import click

from git import Repo, Git
from ..logger import Logger
from ..gitlab.groups_api import GroupsApi
from ..gitlab.projects_api import ProjectsApi
from ..gitlab.users_api import UsersApi
from ..assignment_deploy.assignment_deployer import AssignmentDeployer


class AssignmentSeeder(Logger):
    """This class will create all repos needed for an assignment"""
    def __init__(self, config, class_name, assignment_name, student_name_file, token, stage_mode, team_sets):
        super().__init__(config)
        self.config = config
        self.assignment_json = {}
        self.assignment_name = assignment_name
        self.api_url = 'https://ada-dev.csse.rose-hulman.edu/api/v4/' if stage_mode \
                                            else 'https://ada.csse.rose-hulman.edu/api/v4/'
        self.assignment_json["stageMode"] = True if stage_mode else False
        self.token = token
        self.groups_api = GroupsApi(config, self.api_url)
        self.projects_api = ProjectsApi(config, self.api_url)
        self.users_api = UsersApi(config, self.api_url)
        self.headers = {'PRIVATE-TOKEN': self.token}
        #self.headers = {'Authorization': }
        self.student_names = None
        self.teams = None
        if not team_sets:
            self.student_names = self.get_student_names(student_name_file)
            if self.student_names is None:
                self._warn('Please Create file of name {}\n '
                           'Sample contents are:\n\n'
                           'studentusername1\nstudentusername2\n'
                           .format(student_name_file))
                self._error("Aborting")
        else:
            self.teams = self.get_team_sets(student_name_file)
            if self.teams is None:
                self._warn('Please Create file of name {}\n '
                           'Sample contents are:\n\n'
                           'teamName1,studentusername1,studentusername2\n'
                           'teamName2,studentusername3,studentusername4\n'
                           .format(student_name_file))
                self._error("Aborting")
                return

        self.class_name = class_name
        self.project_ids = []
        self.project_urls = []
        self.project_paths = []
        self.project_names = []
        self.team_sets = team_sets
        #self.grader_backend_url = "https://rosebuild-stage.csse.rose-hulman.edu/api"
        #                          if stage_mode else "https://rosebuild.csse.rose-hulman.edu/api"


    def execute(self):

        self._verbose("Creating Group")
        if self.teams is None and self.student_names is None:
            return

        class_group_id = self.create_class_group()
        if class_group_id == "":
            return


        if self.check_for_assignment():
            return

        seed_repo_name = click.prompt(click.style('Seed Repo Project Name', fg='magenta'),
                                      type=str)

        (data, status) = self.projects_api.search_project(seed_repo_name, self.headers)

        if len(data) > 0:
            seed_repo_url = data[0]["web_url"]
            seed_repo_id = data[0]["id"]
        else:
            self._error("No repo of name {} found".format(seed_repo_name))

        owner_id = click.prompt(click.style('Gitlab user ID', fg='magenta'),
                                type=str)

        due_date = click.prompt(click.style('Due Date (Ex: Jan 7 2019 10:20PM)', fg='magenta'),
                                type=str)

        total_points = click.prompt(click.style('Total Assignment Points', fg='magenta'),
                                    type=str)

        self.assignment_json["gitlabUserId"] = owner_id

        if seed_repo_url == "":
            self._error("No seed repo entered. Cancelling Seeding")
            return

        group_name = self.assignment_name + "-group"

        group_id, namespace = self.create_assignment_group(group_name, class_group_id)

        grouping_json = {
            "gitlabGroupId": group_id
        }
        self.assignment_json["grouping"] = grouping_json

        self._verbose("Group successfully Created")

        self._verbose("Creating All Repo")
        all_project_name = self.assignment_name + "-all"
        all_project_id, all_project_path = self.create_all_repo(all_project_name, owner_id, namespace)

        if all_project_id == "":
            return

        assignment_details_json = {
            "name": group_name,
            "dueDate": due_date,
            "seededRepoId": seed_repo_id,
            "graderRepoId": all_project_id,
            "totalPoints": total_points,
            "manuallyGraded": False
        }

        self.assignment_json["assignment"] = assignment_details_json

        self._verbose("All Repo Created")
        self._verbose("Creating Student Repos")

        if not self.team_sets:
            for student in self.student_names:
                student_project_name = "{}-{}".format(self.assignment_name, student)
                self.create_student_repo(student_project_name, owner_id, seed_repo_url,
                                         namespace, student)
        else:
            self.create_teams(owner_id, seed_repo_url, namespace)

        self._verbose("Repos Created")

        self.add_all_submodules(all_project_name, all_project_path)
        self.groups_api.add_member(group_id, owner_id, 50, self.headers)
        self.create_json_file()




    def create_json_file(self):
        json_obj = json.loads(json.dumps(self.assignment_json))
        deployer = AssignmentDeployer(self.config)
        deployer.set_meta_data(json_obj)
        ret = deployer.execute()
        if ret:
            self._success("Data Successfully Synced")
        else:
            self._error("Data Failed to Sync, saving Data")
            path = click.prompt(click.style('Where should saves be stored?', fg='magenta'),
                                type=str)
            try:
                self._warn("Attempting to create directory " + path)
                os.mkdir(path)

            except OSError as e:
                self._warn("Directory already exists")
            datetime_str = str(datetime.now()).replace(" ", "-").replace(":", "-").replace(".", "-")
            filepath = path + "/" + self.assignment_name + "-" + datetime_str + "-save.json"
            os.open(filepath, os.O_CREAT)
            deployer.save_meta_data(filepath)

    def get_student_names(self, student_name_file):
        try:
            file = open(student_name_file, "r")
        except:
            return None
        return file.readlines()

    def get_team_sets(self, student_name_file):
        try:
            file = open(student_name_file, "r")
        except:
            return None
        lines = file.readlines()
        teams = {}
        for line in lines:
            if not ',' in line:
                continue
            names = line.split(",")
            students = []
            for i in range(1, len(names)):
                students.append(names[i].strip())
            teams[names[0]] = students

        return teams


    def create_class_group(self):
        (data, status) = self.groups_api.search_groups(self.class_name, self.headers)

        if len(data) == 0:
            self._error("Class not found on Ada. Please verify that the class "
                        "has been enabled")
            # form_data = {
            #     "path": self.class_name,
            #     "name": self.class_name,
            # }
            # (data, status) = self.groups_api.create_group(form_data, self.headers)
            # if not "id" in data:
            #     self._error("Class Group could not be successfully created")
            #     return None
            # class_group_id = data["id"]
            # self._success("Class {} created".format(self.class_name))
            return ""

        self._warn("Class of name {} found.".format(self.class_name))
        class_group_id = data[0]["id"]

        return class_group_id

    def check_for_assignment(self):
        (data, status) = self.groups_api.search_groups(self.assignment_name, self.headers)

        if len(data) != 0:
            self._warn("Group with name {} already created. If this group is in "
                       "the class group {}, it will be overriden."
                       .format(self.assignment_name, self.class_name))
            cont = click.prompt(click.style('Continue(Y/N)?', fg='magenta'),
                                type=str)
            if cont != 'Y':
                self._error("Aborting")
                return True

        return False

    def create_assignment_group(self, group_name, class_group_id):
        form_data = {
            "path": group_name,
            "name": group_name,
            "parent_id": class_group_id
        }

        (data, status) = self.groups_api.create_group(form_data, self.headers)
        namespace = self.projects_api.get_namespace(group_name, self.headers)

        return data["id"], namespace

    def create_all_repo(self, all_project_name, owner_id, namespace):
        (data, status) = self.projects_api.search_project(all_project_name, self.headers)

        if len(data) != 0:
            self._warn("All Repo already exists")
            seed_repo_url = click.prompt(click.style('Continue using this all repo? (Y/N)', fg='magenta'),
                                         type=str)
            if seed_repo_url == 'Y':
                all_project_id = data[0]["id"]
                all_project_path = data[0]["web_url"] + ".git"
            else:
                self._error("Exiting Seeding")
                return "", ""
        else:
            form_data = {
                "user_id": owner_id,
                "name": all_project_name,
                "namespace_id": namespace
            }
            (data, status) = self.projects_api.create_project(form_data, self.headers)
            time.sleep(2)
            all_project_id = data["id"]
            all_project_path = data["web_url"] + ".git"
            self._success("Created Repo: {}".format(all_project_name))
        return all_project_id, all_project_path

    def create_student_repo(self, student_project_name, owner_id, seed_repo_url,
                            namespace, student):
        (data, status) = self.projects_api.search_project(student_project_name,
                                                          self.headers)
        if len(data) != 0:
            self._warn("Project {} already exists. Skipping project creation"
                       .format(student_project_name))
            return


        form_data = {
            "user_id": owner_id.strip(),
            "name": student_project_name.strip(),
            "import_url":seed_repo_url.strip(),
            "visibility":"private",
            "namespace_id": namespace
        }

        (data, status) = self.projects_api.create_project(form_data, self.headers)
        #self._error(data)
        time.sleep(2)
        pID = data['id']
        self.project_ids.append(pID)
        pURl = data['web_url']+".git"
        self.project_urls.append(pURl)
        pPath = data['path']
        self.project_paths.append(pPath)
        self._success("Created Repo: {}".format(student_project_name))

        self.add_member(student, pID)

        self.projects_api.unprotect_branch(pID, "master", self.headers)

    def add_member(self, student, pID):
        if not self.team_sets:
            (data, status) = self.users_api.search_user_by_username(student.strip(), self.headers)

            form_data = {
                "id": pID,
                "user_id": data[0]["id"],
                "access_level": 30
            }

            self.projects_api.add_member(pID, form_data, self.headers)
        else:
            for student_name in student:
                (data, status) = self.users_api.search_user_by_username(student_name.strip(), self.headers)

                form_data = {
                    "id": pID,
                    "user_id": data[0]["id"],
                    "access_level": 30
                }

                self.projects_api.add_member(pID, form_data, self.headers)

    def add_all_submodules(self, all_project_name, all_project_path):
        local_project_path = "./"
        full_path = local_project_path+"/"+all_project_name
        Git(local_project_path).clone(all_project_path)
        repo = Repo(full_path)

        for i in range(len(self.project_paths)):
            try:
                repo.create_submodule(name=self.project_paths[i], path=self.project_paths[i],
                                      url=self.project_urls[i], branch='master')
                time.sleep(1)
            except OSError as e:
                self._error("Error occured in creating sub modules")

        file = open(full_path+"/.gitmodules", "r")
        contents = file.read()
        contents = contents.replace("https://", "git@")
        file.close()
        file = open(full_path+"/.gitmodules", "w")
        file.write(contents)
        file.close()
        time.sleep(1)
        repo.git.add(".")
        repo.git.commit("-m", "added submodules")

        origin = repo.remote(name='origin')
        origin.push()
        shutil.rmtree(all_project_name, onerror=self._remove_readonly)

    def create_teams(self, owner_id, seed_repo_url, namespace):
        teams_array = []
        min_team_size = 10
        max_team_size = 1
        for team, members in self.teams.items():
            team_project_name = "{}-{}".format(self.assignment_name, team)
            self.create_student_repo(team_project_name, owner_id, seed_repo_url,
                                     namespace, members)
            teams_array_json = {
                "name": team,
                "members": members
            }
            teams_array.append(teams_array_json)
            if max_team_size < len(members):
                max_team_size = len(members)
            if min_team_size > len(members):
                min_team_size = len(members)
        self.assignment_json["teams"] = teams_array

        override_size = click.prompt(click.style('Detected min/max team size is {} and {}.'
                                                 'Would you like to override this? (Y/N)'
                                                 .format(min_team_size, max_team_size), fg='magenta'),
                                     type=str)
        if override_size != 'N':
            min_team_size = click.prompt(click.style('Enter min team size', fg='magenta'),
                                         type=int)
            max_team_size = click.prompt(click.style('Enter max team size', fg='magenta'),
                                         type=int)

        tomorrow = date.today() + timedelta(days=1)
        create_by = datetime.combine(tomorrow, datetime.min.time())

        team_json = {
            "name": self.assignment_name,
            "minSize": min_team_size,
            "maxSize": max_team_size,
            "createBy":create_by.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.assignment_json["teamSet"] = team_json

    # https://stackoverflow.com/questions/1889597/deleting-directory-in-python/1889686#1889686
    def _remove_readonly(self, func, path, excinfo):
        os.chmod(path, stat.S_IWRITE)
        func(path)
