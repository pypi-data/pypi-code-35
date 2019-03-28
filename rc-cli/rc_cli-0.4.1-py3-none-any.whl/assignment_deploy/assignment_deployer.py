import click
import json
import pathlib
from pymongo import MongoClient
from bson.dbref import DBRef

from ..logger import Logger


class AssignmentDeployer(Logger):
    def __init__(self, config, file_path=None):
        super().__init__(config)
        if file_path != None:
            self.file_path = pathlib.Path.cwd().joinpath(file_path)
        else:
            self.file_path = None
        self.meta_data = None
        self.client = None
        self.db = None
        self.has_invalid_input = False
        self._parse_meta_data()

    def execute(self):
        if self.meta_data is None:
            self._error("Assignment metadata not found")
            return False
        if not self._validate():
            return False
        self.client = MongoClient(self.mongodb_uri)
        self.db = self.client.banner
        try:
            if not self._find_grouping() or self._validate_user():
                return False
            return self._deploy_assignment()
        except:
            return False

    def set_meta_data(self, data):
        self.meta_data = data

    def save_meta_data(self, file_path):
        path = pathlib.Path.cwd().joinpath(file_path)
        with click.open_file(path.as_posix(), 'w') as f:
            f.write(json.dumps(self.meta_data, indent=2))

    def _parse_meta_data(self):
        if self.file_path is None:
            return
        if self.file_path.as_posix().endswith(".json"):
            with click.open_file(self.file_path.as_posix(), 'r') as f:
                self.meta_data = json.load(f)
        else:
            self._error("Expecting .json file")

    def _validate(self):
        return self._validate_basic() and self._validate_team()

    def _validate_basic(self):
        stage_mode = self.meta_data.get('stageMode', None)
        if stage_mode is None:
            self._error("stageMode not provided")
            return False
        self.mongodb_uri = "mongodb://mongodb.default.svc.cluster.local:27017/" \
            if stage_mode else "mongodb://mongodb.default.svc.cluster.local:27017/"

        self.gitlabUserId = self._get_and_check_none(self.meta_data, 'gitlabUserId', "gitlabUserId not provided")
        self.assignment_meta = self._get_and_check_none(self.meta_data, 'assignment', "assignment not provided")
        self.grouping_meta = self._get_and_check_none(self.meta_data, 'grouping', "grouping not provided")

        return self.gitlabUserId and self.assignment_meta and self.grouping_meta

    def _validate_team(self):
        self.team_set_meta = self.meta_data.get('teamSet', None)
        self.teams_meta = self.meta_data.get('teams', None)
        if self.team_set_meta is not None and self.teams_meta is not None:
            self.is_team_assignment = True
        elif self.team_set_meta is None and self.teams_meta is None:
            self.is_team_assignment = False
        else:
            self._error("teamSet or teams not provided")
            return False
        return True

    def _find_grouping(self):
        self.grouping_col = self.db.grouping
        gid = self._get_and_check_none(self.grouping_meta, 'gitlabGroupId', "gitlabGroupId in grouping not provided")
        if self.has_invalid_input:
            return False
        self.grouping = self.grouping_col.find_one({'gitlabGroupId': gid})
        if not self.grouping or self.grouping is None:
            self._error("grouping not found")
            return False
        return True

    def _validate_user(self):
        self.user_col = self.db.user
        self.user = self.user_col.find_one({'gitlabUserId': self.gitlabUserId})
        if not self.user or self.user is None:
            self._error("user not found")
            return False
        for user in self.grouping.authorizedUsers:
            if str(user.id) == str(self.user['_id']):
                return True
        self._error("user not authorized for creating an assignment")
        return False

    def _deploy_assignment(self):
        self.assignment_col = self.db.assignment
        self.assignment = {
            '_class': "edu.rosehulman.csse.rosebuild.models.Assignment",
            'name': self._get_and_check_none(
                self.assignment_meta, 'name', "assignment name not provided"),
            'dueDate': self._get_and_check_none(
                self.assignment_meta, 'dueDate', "assignment dueDate not provided"),
            'seededRepoId': self._get_and_check_none(
                self.assignment_meta, 'seededRepoId', "assignment seededRepoId not provided"),
            'graderRepoId': self._get_and_check_none(
                self.assignment_meta, 'graderRepoId', "assignment graderRepoId not provided"),
            'totalPoints': self._get_and_check_none(
                self.assignment_meta, 'totalPoints', "assignment totalPoints not provided"),
            'manuallyGraded': self._get_and_check_none(
                self.assignment_meta, 'manuallyGraded', "assignment manuallyGraded not provided"),
            'grouping': DBRef("grouping", self.grouping['_id'])
        }
        if self.has_invalid_input:
            return False
        if self.is_team_assignment:
            if not self._create_team_set() or not self._create_teams():
                return False

        self.assignment['_id'] = self.assignment_col.insert_one(self.assignment).inserted_id
        if self.assignment['_id']:
            self._success("\nSuccessfully deployed Assignment {} for {} {}".format(
                self.assignment.name,
                self.grouping.termcode,
                self.grouping.name
            ))
        return self.assignment['_id']

    def _create_team_set(self):
        self.team_set_col = self.db.teamSet
        self.team_set = {
            '_class': "edu.rosehulman.csse.rosebuild.models.TeamSet",
            'name': self._get_and_check_none(self.team_set_meta, 'name', "teamSet name not provided"),
            'grouping': DBRef("grouping", self.grouping['_id']),
            'minSize': self._get_and_check_none(self.team_set_meta, 'minSize', "teamSet minSize not provided"),
            'maxSize': self._get_and_check_none(self.team_set_meta, 'maxSize', "teamSet maxSize not provided"),
            'createBy': self._get_and_check_none(self.team_set_meta, 'createBy', "teamSet createBy not provided")
        }
        if self.has_invalid_input:
            return False
        self.team_set['_id'] = self.team_set_col.insert_one(self.team_set).inserted_id
        self.assignment.teamSet = DBRef("teamSet", self.team_set['_id'])
        return True

    def _create_teams(self):
        self.team_col = self.db.team
        self.teams = []
        for team in self.teams_meta:
            members = []
            is_valid = True
            name = self._get_and_check_none(team, 'name', 'team name not provided')
            if self.has_invalid_input:
                return False
            for username in self._get_and_check_none(team, 'members', "members in team {} not provided".format(name)):
                if self.has_invalid_input:
                    return False
                member = self.user_col.find_one({'email': username + "@rose-hulman.edu"})
                if not member or member is None:
                    self._error(username + "has not logged into Ada")
                    self._error(name + "did not created")
                    is_valid = False
                    break
                members.append(DBRef("user", member['_id']))
            if is_valid or not self.has_invalid_input:
                self.teams.append({
                    '_class': "edu.rosehulman.csse.rosebuild.models.Team",
                    'name': name,
                    'teamSet': DBRef("teamSet", self.team_set['_id']),
                    'members': members
                })
        if self.teams:
            self.team_col.insert_many(self.teams)
        return not self.has_invalid_input

    def _get_and_check_none(self, obj, key, err_msg):
        val = obj.get(key, None)
        if not val or val is None:
            self._error(err_msg)
            self.has_invalid_input = True
            return False
        return val
