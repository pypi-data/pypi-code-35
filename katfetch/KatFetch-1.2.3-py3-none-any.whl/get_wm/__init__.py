"""
GetWM
Get current WM using wmctrl
By Kat Hamer
"""

import subprocess  # Used for spawning wmctrl

def wm():
    """Get current WM"""
    try:
        wm_info = subprocess.check_output(["wmctrl", "-m"]).decode()
        info_lines = wm_info.split("\n")
        wm = info_lines[0].replace("Name: ", "")
        return wm
    except Exception as e:
        print(f"get_wm: {e}")
        return "Unknown"

