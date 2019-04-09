"""This module contains some functions related to Snips services."""

import psutil
import re
from subprocess import check_output


SNIPS_SERVICES = ['snips-analytics', 'snips-asr', 'snips-audio-server',
                  'snips-dialogue', 'snips-hotword', 'snips-injection',
                  'snips-nlu', 'snips-skill-server', 'snips-tts']

VERSION_FLAG = '--version'


def is_installed(service):
    """Check whether the Snips service `service` is installed.

    Args:
        service (string): The Snips service to check. 

    Returns:
        bool: True if the service is installed; False otherwise.

    Example:

        >>> is_installed('snips-nlu')
        True 
    """
    return bool(_version_output(service))

def is_running(service):
    """Check whether the Snips service `service` is running.

    Args:
        service (string): The Snips service to check. 

    Returns:
        bool: True if the service is running; False otherwise.

    Example:

        >>> is_running('snips-nlu')
        True 
    """

    # TODO: Check exceptions?
    # See https://stackoverflow.com/questions/7787120/python-check-if-a-process-is-running-or-not
    return service in (process.name() for process in psutil.process_iter())

def _version_output(service):
    """Return the output of the command `service` with the argument
    '--version'.

    Args:
        service (string): The service to check the version of.

    Returns:
        string: The output of the command `service` with the argument
        '--version', or an empty string if the command is not installed.

    Example:

        >>> _version_output('snips-nlu')
        '1.1.2 (0.62.3) [model_version: 0.19.0]'
    """
    try:
        version_output = check_output([service, VERSION_FLAG]).decode('utf-8')

    except FileNotFoundError:
        version_output = ''

    return version_output

def model_version():
    """Return the model version of Snips NLU.

    Returns:
        string: The model version of Snips NLU, or an empty string if snips-nlu
        is not installed.

    Example:

        >>> model_version()
        '0.19.0'
    """
    version_output = _version_output('snips-nlu')
    try:
        model_version = re.search('\[model_version: (.*)\]',
                                  version_output).group(1)
    except AttributeError, IndexError:
        model_version = ''

    return model_version

def version(second=False):
    """Return the version number of the Snips platform.

    This returns the minimum value of the version numbers of all installed
    Snips services.

    Args:
        second (string, optional): If the argument is `False` or not specified,
            the first version number is returned. If the argument is `True`,
            the second version number is returned.

    Returns:
        string: The version number of the Snips platform, or an empty string if
        no Snips services are installed.

    Examples:

        >>> version()
        '1.1.2'
        >>> version(second=True)
        '0.62.3'
    """

    version_strings = [_version_output(service).strip().split(' ', 1)[1]
                       for service in SNIPS_SERVICES].sort()

    if second:
        versions = [re.search('\((.*)\)', version).group(1)
                    for version in version_strings]
    else:
        versions = [version.split()[0] for version in version_strings]

    return versions.sort()[0]
