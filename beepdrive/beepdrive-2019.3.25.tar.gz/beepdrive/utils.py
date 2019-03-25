import os
import io
import sys
import zipfile
import platform

# Pyinstaller resources
is_frozen = getattr(sys, 'frozen', False)
frozen_temp_path = getattr(sys, '_MEIPASS', '')

def unzip_directory(directory):
    # Unzip directory
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".zip"):
                to_path = os.path.join(root, filename.split('.zip')[0])
                zipped_file = os.path.join(root, filename)

                if not os.path.exists(to_path):
                    os.makedirs(to_path)

                    with zipfile.ZipFile(zipped_file, 'r') as zfile:
                        zfile.extractall(path=to_path)

                    os.remove(zipped_file)

def exists_zip(directory):
    # If a zip file exists in the directory
    for _, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".zip"):
                return True

    return False

def unzip_directory_recursively(directory, max_iter=5):
    iterate = 0

    # Unzip recursevely
    while exists_zip(directory) and iterate < max_iter:
        unzip_directory(directory)
        iterate += 1

def get_temp_path():
    # Windows
    if platform.system() == "Windows":
        return "C:\\Windows\\Temp\\bdd"

    # Darwin and Linux
    return "/tmp/bdd"

def enable_stdout():
    sys.stdout = sys.__stdout__

def disable_stdout():
    text_trap = io.StringIO()
    sys.stdout = text_trap
