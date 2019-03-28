import sys
import urllib
import webbrowser
import logging
import click
import os

class ErrorCatcher():

    def __init__(self):
        self.last_command = ""
        self.command_line_call = "rc "

    def catch_exception(self, etype, value, trace):

        click.secho('An Uncaught Exception has occurred, causing you request to fail', fg='red')
        click.secho('In order to help the Rosebuild team fix this issue, '
                    'we ask that you record this issue on our helpdesk', fg='red')
        click.secho('This tool will autogenerate some ticket information for you, \n'
                    'as well as generate a stacktrace file', fg='red')

        if not click.confirm(click.style('Would you like to log this issue?', fg='magenta')):
            return

        dir = ""
        while dir != "q":
            dir = click.prompt(click.style('Where would you like to generate'
                                           ' the stacktrace.txt file '
                                           '(q to quit)', fg='magenta'),
                               type=str)

            try:
                if not os.path.isdir(dir):
                    os.mkdir(dir)

                file_path = dir + "/stackTrace.txt"
                open(file_path, "w+")
                break
            except OSError as e:
                click.secho('Error in creating directory {}'
                            'Please enter a valid directory path'.format(dir),
                            fg='red')

        if dir == "q":
            click.secho('Quitting', fg='red')
            return

        logging.basicConfig(filename=file_path, level=logging.WARNING)
        logger = logging.getLogger("logger")
        logger.error("Uncaught exception Stacktrace", exc_info=(etype, value,
                                                                trace))
        params = {
            "issue[title]": "Error running {} - {}".format(self.last_command,
                                                           value),
            "issue[description]": self.create_description()
        }
        url_params = urllib.parse.urlencode(params)
        url = "https://ada.csse.rose-hulman.edu/RoseBuild/HelpDesk/issues/new?"
        click.secho('A stacktrace.txt file has been generated in this directory', fg='green')
        click.secho('Please attach this file to the helpdesk ticket', fg='green')
        click.secho('Additionally, please provide any additional details to assist us '
                    'with reproducing and solving this issue', fg='green')

        response = click.prompt(click.style('To proceed to the helpdesk, press enter Y', fg='magenta'),
                                type=str)

        webbrowser.open(url + url_params)




    def set_command(self, command):
        self.last_command = command

    def set_command_long(self, words):
        for i in range(1, len(words)):
            self.command_line_call += "{} ".format(words[i])

    def create_description(self):
        operating_system = sys.platform

        return """# Bug Report\r\r
## Expected Behavior\r
<Enter Expected Outcome>\r\r
## Actual Behavior\r
Error Given. See attached stack trace\r\r
## Steps to Reproduce the Problem\r
<Enter any Preceeding Steps>\r
1. Run command `{}`\r
...\r\r
## Specifications\r
- Browser: Cmd Line\r
- Operating System: {}\r
- Role: Instructor\r\r
## Notes\r
Is there anything you think would be noteworthy to include such as a screenshot
\r
or any browser extension.\r""".format(self.command_line_call, operating_system)
