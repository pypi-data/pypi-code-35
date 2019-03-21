"""
GetShell
Get current shell version
By Kat Hamer
"""

import subprocess  # Used for running shell version commands
import os  # Used to get shell path through environment variable
import re  # Used to parse Bash version text


def get_bash_version():
    """Get Bash version since Bash returns version differently"""
    information_text = subprocess.check_output("bash --version", shell=True).decode()  # Get block of informational text
    version = re.findall(r"\d.\d.\d", information_text)[0]  # Find the first string that looks like X.X.X
    version_string = f"Bash {version}"
    return version_string


def get_other_shell_version():
    """This method to get version works for every shell except Bash as far as I am aware"""
    version = subprocess.check_output("$SHELL --version", shell=True).decode()  # Get version string
    version_string = version.strip()  # Remove newlines and spaces
    return version_string


def version(pretty=True):
    """Returns shell path or version version"""
    shell_path = os.getenv("SHELL")

    if pretty:  # If pretty is enabled display a nice version string
        if shell_path.endswith("bash"):
            return get_bash_version()
        else:
            return get_other_shell_version()
    else:
        return shell_path  # If pretty is disabled return shell path
