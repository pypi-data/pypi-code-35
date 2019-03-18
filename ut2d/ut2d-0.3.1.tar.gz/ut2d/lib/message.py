import sys

from .emoji import EMOJI

HELPER_MSG = {
    'search_tz_begin': 
        EMOJI['face_with_tongue'] + ' '
        ' I am finding your city on popular search engines! Plz wait a sec...',

    'search_conn_failed':
        EMOJI['sad_but_relieved_face'] + ' '
        ' I am sorry, but search city function needs Internet connection to popular search engines && no connection available!'
        ' Please check your Internet connection!',

    'search_tz_failed':
        EMOJI['lying_face'] + ' '
        ' emmm... I cannot find your city on popular search engines!'
        ' Could it be that the input has any typos?'
}

ERROR_MSG = {
    'arg_invalid': 
        EMOJI['face_with_monocle'] + ' '
        ' Your input seems invalid,'
        ' the 1st arg should be either "now" or the unix timestamp'
        ' (10-digit in seconds or 13-digit in milliseconds)',
    
    'tz_fmt_invalid':
        EMOJI['lying_face'] + ' '
        ' Please provide timezone formatted as: GMT+8, or UTC-9.'
        ' Only GMT and UTC as prefix are accepted',
}

MSG_TYPE = {
    0: HELPER_MSG,
    1: ERROR_MSG,
}


def throw_msg(msg_type: int, msg_name: str, sys_exit: bool = False):
    """Throw message spicified by message type and message name.
    
    If sys_exit is set to True, exit the program.
    """
    if (msg_type not in MSG_TYPE) or (msg_name not in MSG_TYPE[msg_type]):
        print(EMOJI['lying_face'] + ' '
              ' something went wrong, plz try again or submit an issue at GitHub.'
              ' Thank you!')
    else:
        print(MSG_TYPE[msg_type][msg_name])

    if sys_exit:
        sys.exit(1)
