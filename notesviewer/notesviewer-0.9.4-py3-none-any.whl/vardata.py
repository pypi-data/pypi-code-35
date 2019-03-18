""" global variable list """

from os.path import expanduser

HOME = expanduser("~")
PROGRAM_NAME = "notesviewer"


# global constant variables
INTERACTIVE_COMMANDS = [
    [
        'list_catagories', 'edit',
        'search', 'settings', 'version', 'quit'
    ],
    [
        'graphical on', 'Scope', 'verbose on',
        'exit', 'quit'
    ],
    ['global', 'catagory', 'note',
     'comment', 'exit', 'quit']
]

# command mode
COMMAND_MODE = INTERACTIVE_COMMANDS[0]

# config file
CONFIG_FILE = "config"
CONFIG_FILE_PATH = HOME + "/" + "." + PROGRAM_NAME + "/" + CONFIG_FILE

# buffer location where all the work is being done
REPO_DIR = HOME + "/" + "notes"

NOTES_ROOT_PATH = ""

GRAPHICAL_DEFAULT = False
VERBOSE_DEFAULT = False
EDITOR_DEFAULT = "vim"
COLOR_ERR_DEFAULT = "white"
COLOR_MSG_DEFAULT = "yellow"
COLOR_NOTE_DEFAULT = "yellow"
COLOR_NOTE_TITLE_DEFAULT = "blue"
COLOR_NOTE_CONTENT_DEFAULT = "green"
COLOR_SEARCH_STRING_DEFAULT = "blue"
COLOR_SEARCH_NOTE_DEFAULT = "green"
DATA_DEFAULT = "file" + ":" + HOME + "/" + "notes"

EDITORS = ['vim', 'emacs']
COLORS = ['red', 'blue', 'green', 'yellow', 'black', 'white']

PROTOCOL_GIT = "git"
PROTOCOL_FILE = "file"

OPTIONS = {
    "graphical": GRAPHICAL_DEFAULT,
    "verbose": VERBOSE_DEFAULT,
    "editor": EDITOR_DEFAULT,
    "color_err": COLOR_ERR_DEFAULT,
    "color_msg": COLOR_MSG_DEFAULT,
    "color_note": COLOR_NOTE_DEFAULT,
    "color_title": COLOR_NOTE_TITLE_DEFAULT,
    "color_content": COLOR_NOTE_CONTENT_DEFAULT,
    "color_search_string": COLOR_SEARCH_STRING_DEFAULT,
    "color_search_notename": COLOR_SEARCH_NOTE_DEFAULT,
    "data_location": DATA_DEFAULT,
}


def set_notes_root_path(path):
    """ set notes_root_path"""

    global NOTES_ROOT_PATH

    NOTES_ROOT_PATH = path


def set_command_mode(interactive_command):
    """ set COMMAND_MODE"""

    global COMMAND_MODE

    COMMAND_MODE = interactive_command
