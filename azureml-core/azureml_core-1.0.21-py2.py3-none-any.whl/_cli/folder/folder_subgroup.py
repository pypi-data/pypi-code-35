# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

from azureml._cli import abstract_subgroup
from azureml._cli import cli_command
from azureml._cli import argument


class FolderSubGroup(abstract_subgroup.AbstractSubGroup):
    """This class defines the folder sub group."""

    def get_subgroup_name(self):
        """Returns the name of the subgroup.
        This name will be used in the cli command."""
        return "folder"

    def get_subgroup_title(self):
        """Returns the subgroup title as string. Title is just for informative purposes, not related
        to the command syntax or options. This is used in the help option for the subgroup."""
        return "folder subgroup commands"

    def get_nested_subgroups(self):
        """Returns sub-groups of this sub-group."""
        return super(FolderSubGroup, self).compute_nested_subgroups(__package__)

    def get_commands(self):
        """ Returns commands associated at this sub-group level."""
        # TODO: Adding commands to a list can also be automated, if we assume the
        # command function name to start with a certain prefix, like _command_*
        commands_list = [self._command_folder_attach()
                         ]
        return commands_list

    def _command_folder_attach(self):
        function_path = "azureml._base_sdk_common.cli_wrapper.cmd_project#attach_project"
        return cli_command.CliCommand("attach", "Convert a local folder on-disk to an AzureMl experiment.",
                                      [argument.EXPERIMENT_NAME.get_required_true_copy(),
                                       argument.PROJECT_PATH,
                                       argument.RESOURCE_GROUP_NAME,
                                       argument.WORKSPACE_NAME], function_path)
