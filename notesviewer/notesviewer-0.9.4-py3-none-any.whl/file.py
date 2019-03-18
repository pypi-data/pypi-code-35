""" Module file """

import os
import stat
import shutil
from termcolor import colored
import notesviewer.vardata
import notesviewer.error

MODES = ("r", "w", "a", "w+")


def open_note(file_context, note, mode):
    """open the meta and return a a fp"""

    # set the path for file_context
    if file_context == 'meta':
        path = notesviewer.vardata.NOTES_ROOT_PATH + "/" + "meta" + "/" + note
    elif file_context == 'content':
        path = (notesviewer.vardata.NOTES_ROOT_PATH + "/"
                + "content" + "/" + note)
    elif file_context == 'link':
        path = notesviewer.vardata.NOTES_ROOT_PATH + "/" + "link" + "/" + note
    elif file_context == 'tag':
        path = notesviewer.vardata.NOTES_ROOT_PATH + "/" + "tags" + "/" + note
    else:
        return notesviewer.error.ERROR_WRONG_NOTE_FILE_CONTEXT

    if mode not in MODES:
        return notesviewer.error.ERROR_WRONG_MODE

    fileptr = open(path, mode)

    if fileptr is None:
        print(colored("Error while trying to open " + note + " --bye",
                      notesviewer.vardata.OPTIONS['color_err']))

    return fileptr


def close_note(filepointer):
    """ close a file pointer"""
    filepointer.close()


def create_config_file():
    """ create config file """

    mode = 0o600 | stat.S_IRUSR

    config_path_dir = (notesviewer.vardata.HOME + "/" + "." +
                       notesviewer.vardata.PROGRAM_NAME)

    if not os.path.exists(config_path_dir):
        os.mkdir(config_path_dir)

    error = os.mknod(notesviewer.vardata.CONFIG_FILE_PATH, mode)
    if error is not None:
        print_err_msg("There was error creating config file " +
                      notesviewer.vardata.CONFIG_FILE_PATH)
        exit(-1)
    else:
        notesviewer.commands.setdefaultconfig(False)


def create_notes_root_path():
    """ creat a note root directory """

    mode = 0o755 | stat.S_IRUSR

    try:
        os.makedirs(notesviewer.vardata.NOTES_ROOT_PATH + "/" + "meta")
        os.makedirs(notesviewer.vardata.NOTES_ROOT_PATH + "/" + "content")
        os.makedirs(notesviewer.vardata.NOTES_ROOT_PATH + "/" + "tags")
        os.makedirs(notesviewer.vardata.NOTES_ROOT_PATH + "/" + "link")
        notesviewer.file.print_info_msg("initalized Root note directory...")
    except OSError:
        notesviewer.file.print_info_msg("Note directory already exists")
        prompt_msg1 = "Would you like to initalize it again(yes/no)\n"
        prompt_msg2 = "This will delete all your notes: "

        prompt = input(prompt_msg1 + prompt_msg2)
        prompt = prompt.lower()
        if prompt == 'yes':
            shutil.rmtree(notesviewer.vardata.NOTES_ROOT_PATH)
            os.makedirs(notesviewer.vardata.NOTES_ROOT_PATH + "/" + "meta")
            os.makedirs(notesviewer.vardata.NOTES_ROOT_PATH + "/" + "content")
            os.makedirs(notesviewer.vardata.NOTES_ROOT_PATH + "/" + "tags")
            os.makedirs(notesviewer.vardata.NOTES_ROOT_PATH + "/" + "link")
            notesviewer.file.print_info_msg("Notes directory re-initalized")


def verify_note(note, file_context):
    """ check note """

    path = getnotepath(note, file_context)
    if os.path.exists(path):
        return True
    return False


def verify_notes_root_path(verbose=False):

    """ check NOTES_ROOT_PATH folder and it's metadata exists"""

    no_root_msg = "No root note directory found"
    run_init_msg = "Use the init command to initalize Notes"
    metadata_msg = "Some of the metadata in notes directory are missing"
    metadata_msg3a = "..Run   " + notesviewer.vardata.PROGRAM_NAME + " check"
    metadata_msg3b = " command  to check what's missing or"
    metadata_msg4a = "..Run   " + notesviewer.vardata.PROGRAM_NAME + " init"
    metadata_msg4b = " command   to initalize base metadata directories"

    if not os.path.exists(notesviewer.vardata.NOTES_ROOT_PATH):
        notesviewer.file.print_err_msg(no_root_msg)
        notesviewer.file.print_info_msg(run_init_msg)
        exit(notesviewer.error.ERROR_NO_ROOT_NOTE)

    # This will be called by cm_check
    if verbose is True:
        missing = []
        if not os.path.exists(getrootpath("meta")):
            notesviewer.file.print_err_msg("Meta folder missing")
            missing.append(notesviewer.error.ERROR_META_MISSING)
        else:
            notesviewer.file.print_info_msg("Meta folder OK")
        if not os.path.exists(getrootpath("content")):
            notesviewer.file.print_err_msg("Content folder missing")
            missing.append(notesviewer.error.ERROR_CONTENT_MISSING)
        else:
            notesviewer.file.print_info_msg("Content folder OK")
        if not os.path.exists(getrootpath("link")):
            notesviewer.file.print_err_msg("Link folder missing")
            missing.append(notesviewer.error.ERROR_LINK_MISSING)
        else:
            notesviewer.file.print_info_msg("Link folder OK")
        if not os.path.exists(getrootpath("tag")):
            notesviewer.file.print_err_msg("tags folder missing")
            missing.append(notesviewer.error.ERROR_TAGS_MISSING)
        else:
            notesviewer.file.print_info_msg("Tags folder OK")
        return missing

    # This will be called in process_args

    if not os.path.exists(getrootpath("meta")) or \
       not os.path.exists(getrootpath("content")) or \
       not os.path.exists(getrootpath("link")) or \
       not os.path.exists(getrootpath("tag")):

        notesviewer.file.print_err_msg(metadata_msg)
        notesviewer.file.print_info_msg(metadata_msg3a + metadata_msg3b)
        notesviewer.file.print_info_msg(metadata_msg4a + metadata_msg4b)
        exit(notesviewer.error.ERROR_METADATA_MISSING)

    return notesviewer.error.ERROR_OK


def verify_empty_note(note, file_context):
    """ check note if empty """

    if os.stat(getnotepath(note, file_context)).st_size == 0:
        return True
    return False


def getnotepath(note, file_context):
    """ return note's path by file_context"""

    if file_context == 'meta':
        return notesviewer.vardata.NOTES_ROOT_PATH + "/" + "meta" + "/" + note
    if file_context == 'content':
        return  \
            notesviewer.vardata.NOTES_ROOT_PATH + "/" + "content" + "/" + note
    if file_context == 'link':
        return notesviewer.vardata.NOTES_ROOT_PATH + "/" + "link" + "/" + note
    if file_context == 'tag':
        return notesviewer.vardata.NOTES_ROOT_PATH + "/" + "tags" + "/" + note
    return notesviewer.error.ERROR_WRONG_NOTE_FILE_CONTEXT


def getrootpath(file_context):
    """ return notes root path by file context """

    if file_context == 'meta':
        return notesviewer.vardata.NOTES_ROOT_PATH + "/" + "meta"
    if file_context == 'content':
        return  \
            notesviewer.vardata.NOTES_ROOT_PATH + "/" + "content"
    if file_context == 'link':
        return notesviewer.vardata.NOTES_ROOT_PATH + "/" + "link"
    if file_context == 'tag':
        return notesviewer.vardata.NOTES_ROOT_PATH + "/" + "tags"
    return notesviewer.error.ERROR_WRONG_NOTE_FILE_CONTEXT


def print_msg(color, msg):
    """ print msg at color base """

    print(colored(msg, color))


def print_err_msg(msg):
    """ print error msg with correct color"""

    print(colored(msg, notesviewer.vardata.OPTIONS['color_err']))


def print_info_msg(msg):
    """ print info msg with correct color"""

    print(colored(msg, notesviewer.vardata.OPTIONS['color_msg']))


def print_list_per_line(mylist, extra_line=True):
    """print a list"""

    if extra_line is False:
        for index in mylist:
            print(
                colored
                (index, notesviewer.vardata.OPTIONS['color_msg']),
                end="")
        return

    for index in mylist:
        print(colored(index, notesviewer.vardata.OPTIONS['color_note']))
