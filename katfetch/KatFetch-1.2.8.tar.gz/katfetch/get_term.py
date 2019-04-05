"""
Get Term
Get current terminal
By Kat Hamer
"""

import psutil  # Used for getting information about processes
import os      # Used to get the PID of our script


"""Some process names don't properly correspond to application names so we map them here"""
terminals = {}


def term():
    """Get current terminal by finding the parent of the parent of our current process"
    This can sometimes produce unexpected results e.g. in a nested shell but works most of the time"""
    process_id = os.getpid()  # Get PID of current process which is our Python program
    process = psutil.Process(process_id)  # Construct a process object out of our PID
    shell_process = process.parent()  # Find out what spawned our script, probably the shell
    terminal_process = shell_process.parent()  # Find out what spawned the shell, hopefully the terminal
    terminal_process_name = terminal_process.name()  # Get the process name of the terminal
    return terminals.get(terminal_process_name, terminal_process_name.title())  # Return a pretty name if we have one

    
