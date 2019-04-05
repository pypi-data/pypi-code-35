from PW_explorer.helper import (
    mkdir_p,
)

import os
import pickle
import sqlite3
import importlib

# File Location Constants:


SRC_TEMP_PICKLE_LOC = '.temp_pickle_data/'
CURRENT_PROJECT_NAME_LOC = SRC_TEMP_PICKLE_LOC + 'current_project_name.pkl'
PROJECT_RESULTS_LOC = 'PWE_Results/'
PROJECT_ASP_INPUT_FOLDER = 'ASP_Input/'
PROJECT_ASP_OUTPUT_FOLDER = 'ASP_Output/'
PROJECT_EXPORTS_FOLDER = 'Exports/'
PROJECT_VISUALIZATIONS_FOLDER = 'Visualizations/'
PROJECT_TEMP_PICKLE_DATA_FOLDER = 'temp_pickle_data/'
CUSTOM_DISTANCE_FUNCTIONS_FOLDER = 'Custom_Distance_Functions'
CUSTOM_VISUALIZATION_FUNCTIONS_FOLDER = 'Custom_Visualization_Functions'


def get_asp_input_folder(project_name):
    """
    :type project_name: string
    """
    loc = PROJECT_RESULTS_LOC + project_name + '/' + PROJECT_ASP_INPUT_FOLDER
    mkdir_p(loc)
    return os.path.abspath(loc)


def get_asp_output_folder(project_name):
    """
    :type project_name: string
    """
    loc = PROJECT_RESULTS_LOC + project_name + '/' + PROJECT_ASP_OUTPUT_FOLDER
    mkdir_p(loc)
    return os.path.abspath(loc)


def get_current_project_name():
    project_name = None
    try:
        with open(CURRENT_PROJECT_NAME_LOC, 'rb') as f:
            project_name = pickle.load(f)
    except IOError:
        project_name = None
    return project_name


def set_current_project_name(project_name):
    mkdir_p(SRC_TEMP_PICKLE_LOC)
    with open(CURRENT_PROJECT_NAME_LOC, 'wb') as f:
        pickle.dump(project_name, f)


def get_save_folder(project_name, data_type):
    data_types_dict = {
        'csv_export': PROJECT_EXPORTS_FOLDER+'csv/',
        'sql_export': PROJECT_EXPORTS_FOLDER+'sql/',
        'msg_export': PROJECT_EXPORTS_FOLDER + 'msg/',
        'h5_export': PROJECT_EXPORTS_FOLDER + 'h5/',
        'pkl_export': PROJECT_EXPORTS_FOLDER + 'pkl/',
        'temp_pickle_data': PROJECT_TEMP_PICKLE_DATA_FOLDER,
        'visualization': PROJECT_VISUALIZATIONS_FOLDER,
        'asp_simple': PROJECT_EXPORTS_FOLDER+'asp_simple/',
        'asp_triples': PROJECT_EXPORTS_FOLDER+'asp_triples/',
    }

    relative_loc = PROJECT_RESULTS_LOC + project_name + '/'

    if data_type in data_types_dict:
        relative_loc += data_types_dict[data_type]
    else:
        relative_loc += data_type + '/'

    mkdir_p(relative_loc)

    return os.path.abspath(relative_loc)


PICKLE_FILE_TYPES = ['dist_matrix', 'dfs', 'relations', 'pws', 'complexities', 'attr_defs', 'meta_data']

def get_file_save_name(project_name, file_type):

    if file_type in PICKLE_FILE_TYPES:
        return file_type + '.pkl'
    return None


def load_from_temp_pickle(project_name, file_type):
    if file_type in PICKLE_FILE_TYPES:
        try:
            with open(get_save_folder(project_name, 'temp_pickle_data') + '/' +
                      get_file_save_name(project_name, file_type), 'rb') as input_file:
                f = pickle.load(input_file)
            return f
        except IOError:
            print("Could not find the project, check project/session name entered.")
            exit(1)


def save_to_temp_pickle(project_name, data, file_type):
    if file_type in PICKLE_FILE_TYPES:
        try:
            with open(get_save_folder(project_name, 'temp_pickle_data') + '/'
                      + get_file_save_name(project_name, file_type), 'wb') as f:
                pickle.dump(data, f)
        except IOError:
            print("Could not find the project, check project/session name entered.")
            exit(1)


def save_to_txt_file(lines, fname):
    with open(fname, 'w') as f:
        f.write('\n'.join(lines))


def get_sql_conn(project_name):
    try:
        conn = sqlite3.connect(get_save_folder(project_name, 'sql_export') + '/' +str(project_name) + ".db")
        return conn
    except sqlite3.Error:
        print("Could not find the associated sqlite database. Please recheck project_name " \
              "or make sure a sql db has been exported using export module")
        exit(1)


def import_custom_module(module_name, module_path):
    """
    Reference: https://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path
    :param module_name: Name of the module to import
    :param module_path: Expected to be an absolute path
    :return: custom_module
    """
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    custom_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(custom_module)
    return custom_module
