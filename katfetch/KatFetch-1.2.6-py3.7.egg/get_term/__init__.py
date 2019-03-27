"""
Get Term
Get current terminal
By Kat Hamer
"""

import psutil  # Used for getting information about processes
import os      # Used to get the PID of our script


"""List of terminals (Needs more)"""
terminals = {"alacritty": "Alacritty",
             "st": "Suckless Terminal (ST)"}


def term():
    """Get current terminal"""
    process_id = os.getpid()  # Get PID of current process which is our Python program
    process = psutil.Process(process_id)  # Construct a process object out of our PID
    shell_process = process.parent()  # Find out what spawned our script, probably the shell
    terminal_process = shell_process.parent()  # Find out what spawned the shell, hopefully the terminal
    terminal_process_name = terminal_process.name()  # Get the process name of the terminal
    return terminals.get(terminal_process_name, terminal_process_name)  # Return a pretty name if we have one

    
