from ..logger import Logger
from urllib.parse import urljoin

from ..gitlab.groups_api import GroupsApi

class GroupDeleter(Logger):

    def __init__(self, config, group_name, token, stage_mode):
        super().__init__(config)
        self.group_name = group_name
        self.api_url = 'https://ada-dev.csse.rose-hulman.edu/api/v4/' if stage_mode else 'https://ada.csse.rose-hulman.edu/api/v4/'
        self.token = token
        self.groups_api = GroupsApi(config, self.api_url)


    def execute(self):
        headers = {'PRIVATE-TOKEN': self.token}
        (data, status) = self.groups_api.search_groups(self.group_name, headers)

        if (status == "401"):
            self._error("Invalid API token")
            return

        if (len(data) == 0):
            self._error("No Group of the name {} found".format(self.group_name))
            return

        if (len(data) > 1):
            self._warn("More than one group with the same name has been found.")
            return

        group_id = data[0]['id']
        response = self.groups_api.delete_group(group_id, headers)

        if (response // 100 == 2):
            self._success("Group Successfully Deleted")
        else:
            self._error("Group Deletion Failed with value: " + str(response))

