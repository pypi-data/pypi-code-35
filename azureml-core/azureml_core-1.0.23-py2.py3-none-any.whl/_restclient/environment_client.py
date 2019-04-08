# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Access EnvironmentClient"""

import requests
import json

from .workspace_client import WorkspaceClient


class EnvironmentClient(WorkspaceClient):
    """Environment client class"""

    def get_rest_client(self, user_agent=None):
        """get service rest client"""
        return self._service_context._get_environment_restclient(user_agent=user_agent)

    def _get_environment_definition(self, name, version=None):
        """
        :param environment_name:
        :type name: str
        :param version:
        :type version: str
        :return Returns the environment definition object:
        """

        cluster_address = self.get_cluster_url()
        headers = self.auth.get_authentication_header()
        workspace_address = self.get_workspace_uri_path()

        environment_url = cluster_address + "/environment/v1.0" + \
            workspace_address + "/environments/" + name

        if version is not None:
            environment_url += "/versions/" + version
        # Else Retrieve the latest version of the environment definition

        response = requests.get(environment_url, headers=headers)

        if response.status_code == 200:
            content = response.content
            if isinstance(content, bytes):
                content = content.decode('utf-8')
            return json.loads(content)
        else:
            message = "Error retrieving the environment definition. Code: {}\n: {}".format(response.status_code,
                                                                                           response.text)
            self._logger.error(message)
            raise Exception(message)

    def _register_environment_definition(self, environment_dict):
        """
        :return Returns the environment definition dictionary from the response:
        """

        environment_name = environment_dict["name"]
        cluster_address = self.get_cluster_url()
        headers = self.auth.get_authentication_header()
        workspace_address = self.get_workspace_uri_path()
        environment_url = cluster_address + "/environment/v1.0" + \
            workspace_address + "/environments/" + environment_name

        body = {'Name': environment_name,
                'python': environment_dict["python"],
                "EnvironmentVariables": environment_dict["environmentVariables"],
                "Docker": environment_dict["docker"],
                "Spark": environment_dict["spark"]
                }

        response = requests.put(
            environment_url, headers=headers, json=body)

        if response.status_code == 200:
            content = response.content
            if isinstance(content, bytes):
                content = content.decode('utf-8')
            return json.loads(content)
        else:
            message = "Error registering the environment definition. Code: {}\n: {}".format(response.status_code,
                                                                                            response.text)
            self._logger.error(message)
            raise Exception(message)

    def _get_image_details(self, name, version=None):
        """
        :param environment_name:
        :type name: str
        :param version:
        :type version: str
        :return Returns the image details:
        """

        cluster_address = self.get_cluster_url()
        headers = self.auth.get_authentication_header()
        workspace_address = self.get_workspace_uri_path()

        environment_url = cluster_address + "/environment/v1.0" + \
            workspace_address + "/environments/" + name

        if version is not None:
            environment_url += "/versions/" + version

        environment_url += "/image"

        response = requests.get(environment_url, headers=headers)

        if response.status_code == 200:
            content = response.content
            if isinstance(content, bytes):
                content = content.decode('utf-8')
            return json.loads(content)
        else:
            message = "Error getting image details. Code: {}\n: {}".format(response.status_code,
                                                                           response.text)
            self._logger.error(message)
            raise Exception(message)
