import os
import sys
import osrs_net


def write(string, filepath):
    try:
        with open(filepath, 'w') as f:
            f.write(string)
        return True

    except Exception as e:
        print('Failed to write data to file: {}, error: {}'.format(filepath, e))


def read(filepath):
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except Exception as e:
        print('Failed to read from file: {}, error: {}'.format(filepath, e))


def create_directory(directory_path):
    try:
        os.makedirs(os.path.dirname(directory_path), exist_ok=True)
    except Exception as e:
        print('Failed to create directory: {}, error: {}'.format(directory_path, e))


def get_base_dir():
    try:
        base_dir = sys._MEIPASS
    except AttributeError:
        base_dir = os.path.dirname(osrs_net.__file__)

    return base_dir
