#!/usr/bin/env python3

"""The Keybase API wrapper.

This library enables the user to communicate with the Keybase command-line
application programmatically via Python.
"""

import json
import subprocess

# TODO: Add more comments and properly format docstrings.


class Keybase:
    """Create an interface with the Keybase application."""

    def __init__(self):
        """Initialize the Keybase class."""
        self.teams = teams()
        self.name = get_username()

    def private_message(self, username):
        """Return a Private Message object with the specified username."""
        return PrivateMessage("{},{}".format(self.name, username))

    @staticmethod
    def unread_pms():
        """Retrieve a dictionary of PMs with unread messages."""
        results = list_unread()
        message_channels = [
            result
            for result in results
            if "topic_name" not in result["channel"].keys()
        ]
        pm_dict = dict()
        for channel in message_channels:
            channel_name = channel["channel"]["name"]
            pm_dict[channel_name] = PrivateMessage(channel_name)
        return pm_dict


class Channel:
    """Interface with a team's channel."""

    def __init__(self, team, name):
        """Initialize the Channel class."""
        self.team = team
        self.name = name

    def get_unread(self):
        """Return a list of unread messages.

        If channel is set, it only includes messages from the specified
        channel. Otherwise, it gets messages from all channels.
        """
        # Craft the generic query.
        query = json.dumps(
            {
                "method": "read",
                "params": {
                    "options": {
                        "channel": {
                            "name": self.team,
                            "members_type": "team",
                            "topic_name": self.name,
                        },
                        "unread_only": True,
                    }
                },
            }
        )
        result = json.loads(chat_api_query(query))
        return parse_messages(result["result"]["messages"])

    def send(self, message):
        """Send a message to this channel."""
        request = {
            "method": "send",
            "params": {
                "options": {
                    "channel": {
                        "name": self.team,
                        "members_type": "team",
                        "topic_name": self.name,
                    },
                    "message": {"body": message},
                }
            },
        }
        return send_message(request)


class Team:
    """Interface with a Keybase team."""

    def __init__(self, name):
        """Initialize the Team class."""
        self.name = name
        self.channels = channels(name)

    def add_member(self, username, role="reader"):
        """Add the specified user to this team.

        The role should be one of the following:
        - reader
        - writer
        - admin
        - owner

        The role will default to reader if none is specified.

        """
        try:
            result = run_command(
                "keybase team add-member {} -u {} -r {} -s".format(
                    self.name, username, role
                )
            )
            return "Success!" in result
        except subprocess.CalledProcessError:
            return False

    def get_members(self):
        """Get a list of the current members in this team."""
        try:
            user_list = list()
            result = run_command(
                "keybase team list-memberships {}".format(self.name)
            )
            for line in result.split("\n"):
                if self.name in line:
                    user_list.append(line.split()[2])
            return user_list
        except subprocess.CalledProcessError:
            return []

    def ignore_request(self, username):
        """Ignore a user's request to join the team."""
        try:
            result = run_command(
                "keybase team ignore-request {} -u {}".format(
                    self.name, username
                )
            )
            return "Success!" in result
        except subprocess.CalledProcessError:
            return False

    def join_requests(self, tries=0):
        """Retrieve a dictionary of team access requests."""
        try:
            result = run_command(
                "keybase team list-requests -t {}".format(self.name)
            )
        except subprocess.CalledProcessError:
            if tries == 3:
                subprocess.check_output("keybase ctl restart", shell=True)
            elif tries == 6:
                raise
            return self.join_requests(tries=(tries + 1))
        if "No requests at this time." in result:
            return list()
        return [
            line.split()[1]
            for line in result.split("\n")
            if "wants to join" in line
        ]

    def remove_member(self, username):
        """Remove the specified user from this team."""
        try:
            result = run_command(
                "keybase team remove-member {} -u {} -f".format(
                    self.name, username
                )
            )
            return "Success!" in result
        except subprocess.CalledProcessError:
            return False

    def unread_channels(self):
        """Retrieve a dictionary of Channel objects with unread messages."""
        results = list_unread()
        channel_list = [
            result["channel"]["topic_name"]
            for result in results
            if "topic_name" in result["channel"].keys()
            and result["channel"]["name"] == self.name
        ]
        channel_dict = dict()
        for channel in channel_list:
            channel_dict[channel] = self.channels[channel]
        return channel_dict


class PrivateMessage:
    """Create a reference to a specific private message conversation."""

    def __init__(self, name):
        """Initialize the PrivateMessage class."""
        self.name = name

    def get_unread(self):
        """Retrieve a list of unread messages from this PM."""
        query = json.dumps(
            {
                "method": "read",
                "params": {
                    "options": {
                        "channel": {"name": self.name},
                        "unread_only": True,
                    }
                },
            }
        )
        result = json.loads(chat_api_query(query))
        return parse_messages(result["result"]["messages"])

    def send(self, message):
        """Send a private message to the specified user."""
        # Format the message.
        request = {
            "method": "send",
            "params": {
                "options": {
                    "channel": {"name": self.name},
                    "message": {"body": message},
                }
            },
        }
        return send_message(request)


def channels(team):
    """Return a dictionary of Channel objects for the specified team."""
    channel_dict = dict()
    for channel in list_channels(team):
        channel_dict[channel] = Channel(team, channel)
    return channel_dict


def chat_api_query(query):
    """Send a JSON query to the Keybase Chat API and retrieve a result.

    Input: String-encdoded JSON query.
    Output: String-encoded JSON result.
    """
    return run_command("keybase chat api -m '{}'".format(query))


def get_username():
    """Get the name of the user currently logged in."""
    result = run_command("keybase status")
    username = result.split("\n")[0].split(":")[-1].strip()
    return username


def list_channels(team):
    """Return a list of channel names for the specified team."""
    # Get the channel list.
    result = run_command("keybase chat list-channels '{}'".format(team))
    # Extract lines which list actual channels.
    results = [line for line in result.split("\n") if "#" in line]
    # Extract actual channel names.
    channel_list = [result.split()[0][1:] for result in results]
    # Return extracted channels.
    return channel_list


def list_inbox():
    """List the conversations in the inbox."""
    result = json.loads(chat_api_query(json.dumps({"method": "list"})))
    return result["result"]["conversations"]


def list_teams():
    """Retrieve a dict of teams in which the user is a member."""
    # Retrieve the list of teams.
    result = run_command("keybase team list-memberships")
    # Parse it into a list, skipping the first line because it just lists the
    # column names.
    team_list = [item for item in result.split("\n")[1:-1]]
    team_dict = dict()
    for team in team_list:
        [name, roles, member_count] = [
            item.strip() for item in team.split("    ") if item != ""
        ]
        roles = roles.split(", ")
        team_dict[name] = {"roles": roles, "member_count": member_count}
    return team_dict


def list_unread():
    """Retrieve a list of channels containing unread messages."""
    results = list_inbox()
    return [result for result in results if result["unread"]]


def parse_messages(message_list):
    """Parse a list of messages and return the important data.

    The output is a list of lists, with the following structure:

        [(source, sender, content), (source, sender, content), ...]

    The source is a reference to the channel or PM where the message was
    received. The sender is the user who sent the message. And the content is
    the text they sent in their message.

    """
    outgoing_list = list()
    for message in message_list:
        if "topic_name" in message["msg"]["channel"].keys():
            # This is a message in a team channel.
            team_name = message["msg"]["channel"]["name"]
            channel_name = message["msg"]["channel"]["topic_name"]
            source = Channel(team_name, channel_name)
        else:
            # This is a private message.
            channel_name = message["msg"]["channel"]["name"]
            source = PrivateMessage(channel_name)
        sender = message["msg"]["sender"]["username"]
        content_type = message["msg"]["content"]["type"]
        if content_type != "text":
            # For now, we're only processing text data.
            continue
        content = message["msg"]["content"]["text"]["body"].strip()
        outgoing_list.append((source, sender, content))
    return outgoing_list


def run_command(command_string):
    """Execute a console command and retrieve the result."""
    attempts = 0
    while True:
        try:
            return subprocess.check_output(
                command_string,
                stderr=subprocess.STDOUT,
                shell=True,
                timeout=10,
            ).decode()
        except subprocess.TimeoutExpired:
            if attempts > 3:
                raise
            subprocess.check_output("keybase ctl restart", shell=True)
            attempts += 1


def send_message(request):
    """Send the provided message with the chat API."""
    # Format the message and escape any single-quotes.
    outgoing_message = json.dumps(request).replace("'", "\u2019")
    # Send the message and retrieve the result.
    result = json.loads(chat_api_query(outgoing_message))["result"]
    # Inform them whether the message sent (True) or failed (False).
    return result["message"] == "message sent"


def teams(admin=False):
    """Return a dict of Team objects.

    If admin is set to True, this will return a dict of teams in which the user
    is an admin or an owner.
    """
    result = dict()
    team_dict = list_teams()
    for (name, team) in team_dict.items():
        if "admin" in team["roles"] or "owner" in team["roles"] or not admin:
            result[name] = Team(name)
    return result


def zero_width_joiner():
    """Return the unicode character for the zero-width joiner.

    This is useful for making compound emoji. For example,
    :waving_black_flag: + zwj + :skull_and_crossbones: = pirate flag.
    """
    return "\u200d"
