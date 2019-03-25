import re
import os
from pathlib import Path

def get_working_dir():
    wd_path = os.getcwd()
    directory = re.search(r"[^/]+$", wd_path)
    return directory.group(0)

def mk_file_path(dir):
    home = str(Path.home())
    return home + "/devtrack_projects/" + dir + ".csv"

def check_file(path):
    if os.path.isfile(path):
        return True
    else:
        return False
