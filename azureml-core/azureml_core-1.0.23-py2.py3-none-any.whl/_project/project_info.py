# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import json
import os
import shutil
from azureml.exceptions import UserErrorException
from collections import namedtuple

import azureml._project.file_utilities as file_utilities

_legacy_project_filename = "project.json"
_project_filename = "config.json"


def add(project_id, scope, project_path, is_config_file_path=False):
    """
    Creates project info file

    :type project_id: str
    :type scope: str
    :type project_path: str

    :rtype: None
    """
    if is_config_file_path:
        project_file_path = project_path
    else:
        config_directory = os.path.join(project_path, file_utilities.azureml_configuration_directory_name)
        file_utilities.create_directory(config_directory, True)
        project_file_path = os.path.join(config_directory, _project_filename)
    # We overwriting if project.json exists.
    with open(project_file_path, "w") as fo:
        info = ProjectInfo(project_id, scope)
        fo.write(json.dumps(info.__dict__))


def get_workspace_info(found_path):
    with open(found_path, 'r') as config_file:
        config = json.load(config_file)

    # Checking the keys in the config.json file to check for required parameters.
    scope = config.get('Scope')
    if not scope:
        if not all([k in config.keys() for k in ('subscription_id', 'resource_group', 'workspace_name')]):
            raise UserErrorException('The config file found in: {} does not seem to contain the required '
                                     'parameters. Please make sure it contains your subscription_id, '
                                     'resource_group and workspace_name.'.format(found_path))
        # User provided ARM parameters take precedence over values from config.json
        subscription_id_from_config = config['subscription_id']
        resource_group_from_config = config['resource_group']
        workspace_name_from_config = config['workspace_name']
    else:
        pieces = scope.split('/')
        # User provided ARM parameters take precedence over values from config.json
        subscription_id_from_config = pieces[2]
        resource_group_from_config = pieces[4]
        workspace_name_from_config = pieces[8]
    return (subscription_id_from_config, resource_group_from_config, workspace_name_from_config)


def get(project_path, no_recursive_check=False):
    """
    Get ProjectInfo for specified project

    :type project_path: str
    :param no_recursive_check:
    :type no_recursive_check: bool
    :rtype: ProjectInfo
    """
    while True:
        for config_path in [
                file_utilities.configuration_directory_name,
                file_utilities.legacy_configuration_directory_name]:
            legacy_info_path = os.path.join(project_path, config_path, _legacy_project_filename)
            info_path = os.path.join(project_path, config_path, _project_filename)
            if os.path.exists(legacy_info_path):
                with open(legacy_info_path) as info_json:
                    info = json.load(info_json)
                    info = namedtuple("ProjectInfo", info.keys())(*info.values())
                    return info
            if os.path.exists(info_path):
                with open(info_path) as info_json:
                    info = json.load(info_json)
                    info = namedtuple("ProjectInfo", info.keys())(*info.values())
                    return info

        parent_dir = os.path.dirname(project_path)
        if project_path == parent_dir:
            break
        else:
            project_path = parent_dir

        if no_recursive_check:
            return None
    return None


def delete_project_json(project_path):
    """
    Deletes the project.json from the project folder specified by project_path.
    :return: None, throws an exception if deletion fails.
    """
    for config_path in [file_utilities.configuration_directory_name,
                        file_utilities.legacy_configuration_directory_name]:
        legacy_info_path = os.path.join(project_path, config_path, _legacy_project_filename)
        info_path = os.path.join(project_path, config_path, _project_filename)
        if os.path.exists(legacy_info_path):
            os.remove(legacy_info_path)
        if os.path.exists(info_path):
            os.remove(info_path)


def delete(project_path):
    """
    Deletes the metadata folder containing project info

    :type project_path: str

    :rtype: None
    """
    config_directory = os.path.join(project_path, file_utilities.configuration_directory_name)
    if os.path.isdir(config_directory):
        shutil.rmtree(config_directory)
    legacy_config_directory = os.path.join(project_path, file_utilities.legacy_configuration_directory_name)
    if os.path.isdir(legacy_config_directory):
        shutil.rmtree(legacy_config_directory)


class ProjectInfo(object):
    def __init__(self, project_id, scope):
        """
        :type project_id: str
        :type scope: str
        """
        # Uppercase to work with existing JSON files
        self.Id = project_id
        self.Scope = scope
