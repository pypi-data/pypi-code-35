#!/usr/bin/env python3

from json import load as json_load
from pathlib import Path
from os import environ

from redminelib import Redmine


class RedmineTimeTracking:
    def __init__(self):
        """Instanciate attributes."""

        self.config_dir_path = environ.get("G2C_CONFIG_HOME", default="~/.config/g2c")
        self.config_file_path = (
            Path(self.config_dir_path, "redmine.json").expanduser().resolve()
        )
        self.config = self._get_config(self.config_file_path)
        self.redmine = self._get_redmine(self.config)

    def _get_config(self, path):
        """Get config parameters.

        :param path: Path to the JSON configuration file
        :type path: str
        :return: Configuration parameters
        :rtype: dict
        """

        config = dict()

        with open(path) as config_fh:
            config = json_load(config_fh)

        return config

    def _get_redmine(self, config):
        """Get Redmine resource object.

        :param config: Connection parameters
        :type config: dict
        :return: Redmine connection
        :rtype: redminelib.Redmine
        """

        return Redmine(**config)

    def _get_issue(self, redmine, issue_id):
        """Get Redmine issue resource object.

        :param redmine: Redmine connection object
        :type redmine: Redmine
        :param issue_id: Redmine issue ID
        :type issue_id: int
        :return: Redmine issue object
        :rtype: redminelib.resources.Issue
        """

        return self.redmine.issue.get(issue_id)

    def _get_project(self, project_id, include=None):
        """Get Redmine project resource object

        :param project_id: Redmine project ID
        :type project_id: int
        :param include: Optional fields to include in project entry, defaults to None
        :param include: str, optional
        :return: Redmine project object
        :rtype: redminelib.resources.Project
        """

        return self.redmine.project.get(project_id, include=include)

    def add_time(self, issue_id, hours, spent_on, comments):
        """Add time tracking entry into the given Redmine issue.

        :param issue_id: Redmine issue ID
        :type issue_id: int
        :param hours: Duration of the tasks
        :type hours: float
        :param spent_on: Date of the tasks
        :type spent_on: datetime.date
        :param comments: Description of the task
        :type comments: str
        """

        issue = self._get_issue(self.redmine, issue_id)
        project = self._get_project(issue.project.id, include="time_entry_activities")
        activity_id = project.time_entry_activities[0]["id"]
        # TODO: proper handling of activities
        # for activity in project.time_entry_activities:
        #     if activity["name"].lower() == activity.lower():
        #         activity_id = activity["id"]

        return self.redmine.time_entry.create(
            issue_id=issue_id,
            hours=hours,
            spent_on=spent_on,
            comments=comments,
            activity_id=activity_id,
        )

