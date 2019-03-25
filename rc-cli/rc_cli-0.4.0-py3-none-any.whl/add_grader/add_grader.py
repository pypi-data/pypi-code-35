import click
import time
import os

from ..logger import Logger
from ..gitlab.groups_api import GroupsApi
from ..gitlab.projects_api import ProjectsApi
from ..gitlab.users_api import UsersApi
from git import Repo, Git

class AddGrader(Logger):

    def __init__(self, config, class_name, assistant, professor, token, stage_mode):
        super().__init__(config)
        self.api_url = 'https://ada-dev.csse.rose-hulman.edu/api/v4/' if stage_mode else 'https://ada.csse.rose-hulman.edu/api/v4/'
        self.token = token
        self.groups_api = GroupsApi(config, self.api_url)
        self.projects_api = ProjectsApi(config, self.api_url)
        self.users_api = UsersApi(config, self.api_url)
        self.headers = {'PRIVATE-TOKEN': self.token}
        self.class_name = class_name
        self.has_assistants = assistant != ""
        self.has_professors = professor != ""
        self.assistants = assistant.split(',')
        self.professors = professor.split(',')

    def execute(self):
        (data, status) = self.groups_api.search_groups(self.class_name, self.headers)
        if len(data) == 0:
            self._warn("No class with name {} found".format(self.class_name))
            return

        class_group_id = data[0]["id"]

        self.add_assistant(class_group_id)
        self._success("All TAs added")
        self.add_professor(class_group_id)
        self._success("All Professors added")



    def add_assistant(self, class_group_id):
        if self.has_assistants:
            for assistant in self.assistants:

                (data, status) = self.users_api.search_user_by_username(assistant.strip(), self.headers)

                if len(data) == 0:
                    self._warn("TA of name {} not found. Skipping".format(assistant))
                    continue

                assistant_id = data[0]["id"]

                self.groups_api.add_member(class_group_id, assistant_id, 40, self.headers)
                self._success("Added TA {}".format(assistant))

    def add_professor(self, class_group_id):
        if self.has_professors:

            for professor in self.professors:

                (data, status) = self.users_api.search_user_by_username(professor.strip(), self.headers)

                if len(data) == 0:
                    self._warn("Professor of name {} not found. Skipping".format(professor))
                    continue

                assistant_id = data[0]["id"]

                self.groups_api.add_member(class_group_id, assistant_id, 40, self.headers)
                self._success("Added TA {}".format(professor))