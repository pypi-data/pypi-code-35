""" config module """

import os
import configparser
import notesviewer.vardata
import notesviewer.file


def loadconfig():
    """ load config file into the OPTIONS dictionary """

    # return False if there is no config file
    if not verifyconfigfile():
        notesviewer.file.create_config_file()

    # read config file
    config = configparser.ConfigParser()
    config.read(notesviewer.vardata.CONFIG_FILE_PATH)

    # return False if no setttings section
    if not config.has_section('settings'):
        return False

    # load each setting option if
    # available else it will go with default
    if config.has_option('settings', 'graphical'):
        notesviewer.vardata.OPTIONS['graphical'] = \
            config.get('settings', 'graphical')
        if config.has_option('settings', 'verbose'):
            notesviewer.vardata.OPTIONS['verbose'] = \
                config.get('settings', 'verbose')
        if config.has_option('settings', 'editor'):
            notesviewer.vardata.OPTIONS['editor'] = \
                config.get('settings', 'editor')
        if config.has_option('settings', 'color_err'):
            notesviewer.vardata.OPTIONS['color_err'] = \
                config.get('settings', 'color_err')
        if config.has_option('settings', 'color_msg'):
            notesviewer.vardata.OPTIONS['color_msg'] = \
                config.get('settings', 'color_msg')
        if config.has_option('settings', 'color_note'):
            notesviewer.vardata.OPTIONS['color_note'] = \
                config.get('settings', 'color_note')
        if config.has_option('settings', 'color_title'):
            notesviewer.vardata.OPTIONS['color_title'] = \
                config.get('settings', 'color_title')
        if config.has_option('settings', 'color_content'):
            notesviewer.vardata.OPTIONS[
                'color_content'] = \
                config.get('settings', 'color_content')
        if config.has_option(
                'settings', 'color_search_string'):
            notesviewer.vardata.OPTIONS[
                'color_search_string'] = \
                config.get('settings',
                           'color_search_string')
        if config.has_option('settings',
                             'color_search_notename'):
            notesviewer.vardata.OPTIONS[
                'settings',
                'color_search_notenmae'] = \
                config.get('settings',
                           'color_search_notename')
        if config.has_option('settings',
                             'data_location'):
            notesviewer.vardata.OPTIONS[
                'data_location'] = \
                config.get('settings',
                           'data_location')
    return True


def setdefaultconfig(verbose):
    """ set the default configuration.. overwriting old configuration"""

    # add setting and options
    config = configparser.ConfigParser()
    config.add_section("settings")
    config.set("settings", "graphical", str(
        notesviewer.vardata.GRAPHICAL_DEFAULT))
    config.set("settings", "verbose", str(
        notesviewer.vardata.VERBOSE_DEFAULT))
    config.set("settings", "editor",
               notesviewer.vardata.EDITOR_DEFAULT)
    config.set("settings", "color_err",
               notesviewer.vardata.COLOR_ERR_DEFAULT)
    config.set("settings", "color_msg",
               notesviewer.vardata.COLOR_MSG_DEFAULT)
    config.set("settings", "color_note",
               notesviewer.vardata.COLOR_NOTE_DEFAULT)
    config.set("settings", "color_title",
               notesviewer.vardata.COLOR_NOTE_TITLE_DEFAULT)
    config.set("settings", "color_content",
               notesviewer.vardata.COLOR_NOTE_CONTENT_DEFAULT)
    config.set("settings", "color_search_string",
               notesviewer.vardata.COLOR_SEARCH_STRING_DEFAULT)
    config.set("settings", "color_search_notename",
               notesviewer.vardata.COLOR_SEARCH_NOTE_DEFAULT)
    config.set("settings", "data_location",
               notesviewer.vardata.DATA_DEFAULT)

    # write to CONFIG_FILE
    with open(notesviewer.vardata.CONFIG_FILE_PATH, "w") as filepointer:
        config.write(filepointer)

    if verbose is True:
        notesviewer.file.print_info_msg("Default settings copied")


def setconfig(key, value):
    """ set config """

    if key == "graphical":
        if value not in ("True", "False"):
            notesviewer.file.print_err_msg(
                key + " value can only be True or False"
            )
            exit(0)

    elif key == "verbose":
        if value not in ("True", "False"):
            notesviewer.file.print_err_msg(
                key + " value can only be True or False"
            )
            exit(0)

    elif key == "editor":
        if value not in ("vim", "vi", "emacs", "nano", "pico"):
            notesviewer.file.print_err_msg(
                "You can only set these editors: vim, vi, emacs, nano, pico"
            )
            exit(0)

    elif key in (
            "color_msg",
            "color_err",
            "color_note",
            "color_title",
            "color_content",
            "color_search_string",
            "color_search_notename"):
        if value not in notesviewer.vardata.COLORS:
            notesviewer.file.print_err_msg(
                "You can only set these colors "
                + ", ".join(notesviewer.vardata.COLORS))
            exit(0)

    elif key == "data_location":
        if value.split(":", 1)[0] not in "file":
            notesviewer.file.print_err_msg(
                "data_location can only set these protocols: file"
            )
            exit(0)
        if not os.path.isdir(value.split(":", 1)[1]):
            notesviewer.file.print_err_msg(
                "dat_location path is not a directory"
            )
            exit(0)

    else:
        notesviewer.file.print_err_msg("There is no such option " + key)
        exit(0)

    config = configparser.ConfigParser()
    config.read(notesviewer.vardata.CONFIG_FILE_PATH)

    config.set("settings", key, value)

    # write to CONFIG_FILE
    with open(notesviewer.vardata.CONFIG_FILE_PATH, "w") as filepointer:
        config.write(filepointer)


def verifyconfigfile():
    """verify if config file is found """
    if os.path.isfile(notesviewer.vardata.CONFIG_FILE_PATH) is True:
        return True
    return False


def verify_key(key):
    " verify if the key is a valid option """

    for k in notesviewer.vardata.OPTIONS.keys():
        if key == k:
            return True
    return False


def verify_key_value(key, val):
    """verify if a value is a valid option for a key"""

    if key in ("verbose", "graphical"):
        if val in ("true", "false"):
            return True
    if key == "editor":
        if val in notesviewer.vardata.EDITORS:
            return True
    if key in ("color_err", "color_cata", "color_note"):
        if val in notesviewer.vardata.COLORS:
            return True
    return False


def checksection(conf, section):
    """ check to see if config has a section"""
    conf.read(notesviewer.vardata.CONFIG_FILE_PATH)
    if conf.has_section(section):
        return True
    return False


def showconfig():
    """ Main funcation for showconfig() """

    if verifyconfigfile() is False:
        print("There is no " + notesviewer.vardata.CONFIG_FILE_PATH)
        return False

    config = configparser.ConfigParser()
    config.read(notesviewer.vardata.CONFIG_FILE_PATH)

    # get items from config
    items = dict(config.items("settings"))
    for key, value in zip(items.keys(), items.values()):
        print(key + ":" + value)

    return True


def printconfigoptoin(conf, option):
    """ print an option"""
    print(conf.get('settings', option))


def set_data_location():
    """ set data location """
    if get_data_location_type() == "file":
        notesviewer.vardata.set_notes_root_path(
            get_data_location_source())


def get_data_location_source():
    """ get data location source """

    return notesviewer.vardata.OPTIONS['data_location'].split(":", 1)[1]


def get_data_location_type():
    """ get data location type """
    return notesviewer.vardata.OPTIONS['data_location'].split(":")[0]
