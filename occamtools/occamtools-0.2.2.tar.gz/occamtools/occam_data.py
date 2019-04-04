import os
import numpy as np
import warnings
import json
from tqdm import tqdm
from occamtools.read_xyz import _are_floats, Xyz
from occamtools.read_fort1 import Fort1
from occamtools.read_fort7 import Fort7


def _check_internal_consistency(a, b):
    ignore = ['file_name', 'num_lines']
    a_vars, b_vars = a.__dict__, b.__dict__
    consistent = True
    for k in a_vars:
        if (k in b_vars) and (k not in ignore):
            warn = False
            a_val = a_vars[k]
            b_val = b_vars[k]
            if _are_floats(a_val, b_val):  # These attributes are numbers
                if not np.allclose(a_val, b_val):
                    warn = True
            elif isinstance(a_val, str) and isinstance(b_val, str):
                if not (a_val == b_val):
                    warn = True
            if warn:
                class_a, class_b = type(a).__name__, type(b).__name__
                warn_str = ('\nData is not internally consistent\n\n'
                            + '->' + str(class_a) + ' from file ' + a.file_name
                            + ': ' + str(a_val) + '\n\n'
                            + '->' + str(class_b) + ' from file ' + b.file_name
                            + ': ' + str(b_val))
                consistent = False
                warnings.warn(warn_str)
    return consistent


def _check_internal_consistency_all(fort1, fort7, xyz):
    consistent_1_7 = _check_internal_consistency(fort1, fort7)
    consistent_1_xyz = _check_internal_consistency(fort1, xyz)
    consistent_7_xyz = _check_internal_consistency(fort7, xyz)
    if consistent_1_7 and consistent_1_xyz and consistent_7_xyz:
        return True
    else:
        return False


def _open_fort_files(fort1, fort7, xyz, silent, which=None):
    if which is None:
        f1 = Fort1(fort1)
        f7 = Fort7(fort7)
        x = Xyz(xyz)
    else:
        if which == 0:
            f1 = fort1
            f7 = os.path.join(os.path.dirname(fort1), 'fort.7')
            x = os.path.join(os.path.dirname(fort1), 'fort.8')
        elif which == 1:
            f1 = os.path.join(os.path.dirname(fort7), 'fort.1')
            f7 = fort7
            x = os.path.join(os.path.dirname(fort7), 'fort.8')
        elif which == 2:
            f1 = os.path.join(os.path.dirname(xyz), 'fort.1')
            f7 = os.path.join(os.path.dirname(xyz), 'fort.7')
            x = xyz
        f1 = Fort1(f1)
        f7 = Fort7(f7)
        x = Xyz(x)

    for f in (f1, f7, x):
        f.read_file(silent=silent)
    return f1, f7, x


def _check_npy_dump_exists(file_name):
    class_dir = None
    if os.path.isdir(file_name):
        class_dir = os.path.join(file_name, 'class_data')
    elif os.path.exists(file_name):
        class_dir = os.path.join(os.path.dirname(file_name), 'class_data')
    else:
        raise FileNotFoundError('Could not find file, ' + file_name)
    exists = False
    if os.path.exists(class_dir):
        if os.path.exists(os.path.join(class_dir, 'x.npy')):
            exists = True
    return exists, class_dir


def _check_constructor_input(*args, silent=False):
    if len(args) == 3:
        fort1, fort7, xyz = args
        if (isinstance(fort1, Fort1) and isinstance(fort7, Fort7)
                and isinstance(xyz, Xyz)):
            return fort1, fort7, xyz
        elif (isinstance(fort1, str) and isinstance(fort7, str)
                and isinstance(xyz, str)):
            return _open_fort_files(fort1, fort7, xyz, silent)
        elif isinstance(fort1, str):
            return _open_fort_files(fort1, fort7, xyz, silent, which=0)
        elif isinstance(fort7, str):
            return _open_fort_files(fort1, fort7, xyz, silent, which=1)
        elif isinstance(xyz, str):
            return _open_fort_files(fort1, fort7, xyz, silent, which=2)
        else:
            raise ValueError('OccamData constructor input not recognized as '
                             'Fort1/Fort7/Xzy objects or (one or more) file '
                             'paths.')
    elif len(args) == 1:
        if not isinstance(args[0], str):
            raise TypeError('OccamData constructor called with a single input '
                            'must be a file path, not ' + repr(args[0]))
        if isinstance(args[0], str) and (not os.path.exists(args[0])):
            raise FileNotFoundError('File provided in OccamData constructor '
                                    'not found, ' + args[0])

        extension = os.path.basename(args[0]).split('.')[-1]
        if extension == str(1):
            f1 = args[0]
            f7 = os.path.join(os.path.dirname(f1), 'fort.7')
            x = os.path.join(os.path.dirname(f1), 'fort.8')
        elif extension == str(7):
            f7 = args[0]
            f1 = os.path.join(os.path.dirname(f7), 'fort.1')
            x = os.path.join(os.path.dirname(f7), 'fort.8')
        elif extension == str(8) or extension == 'xyz':
            x = args[0]
            f1 = os.path.join(os.path.dirname(x), 'fort.1')
            f7 = os.path.join(os.path.dirname(x), 'fort.7')
        elif os.path.isdir(args[0]):
            f1 = os.path.join(args[0], 'fort.1')
            f7 = os.path.join(args[0], 'fort.7')
            x = os.path.join(args[0], 'fort.8')
        return _open_fort_files(f1, f7, x, silent)


class OccamData:
    save_dir = 'class_data'

    def __init__(self, *args, load_from_npy=True, silent=False):
        npy_loaded = False
        if len(args) == 1 and load_from_npy:
            check, class_path = _check_npy_dump_exists(args[0])
            if check:
                self.load(class_path, silent=silent)
                npy_loaded = True
        if not npy_loaded:
            fort1, fort7, xyz = _check_constructor_input(*args, silent=silent)
            self.consistent = _check_internal_consistency_all(fort1, fort7,
                                                              xyz)
            ignore = ['file_name', 'n_time_steps_', 'file_contents',
                      'comment_format_known', 'num_lines']
            for f in (fort1, fort7, xyz):
                for key in f.__dict__:
                    if key not in ignore:
                        setattr(self, key, f.__dict__[key])
            self.fort1_file_name = fort1.file_name
            self.fort7_file_name = fort7.file_name
            self.xyz_file_name = xyz.file_name
            self.save()

    def save(self, overwrite=False):
        self.save_path = os.path.join(os.path.dirname(self.fort1_file_name),
                                      self.save_dir)
        if (os.path.exists(self.save_path)):
            if not overwrite:
                return False
        else:
            os.mkdir(self.save_path)
        self._save_arrays()
        self._delete_array_attributes()
        self._save_class()
        self._load_arrays(self.save_path, silent=True)
        return True

    def load(self, class_path, silent=False):
        self._load_arrays(class_path, silent=silent)
        self._load_class(class_path)

    def _load_arrays(self, class_path, silent):
        files = os.listdir(class_path)
        non_npy_files = []
        for f in files:
            if f.split('.')[-1] != 'npy':
                non_npy_files.append(f)
        for f in non_npy_files:
            files.remove(f)

        if not silent:
            print('Loading data from .npy files in directory:\n'
                  + os.path.abspath(class_path) + '/')
            with tqdm(total=len(files)) as pbar:
                for npy_file in files:
                    attribute_name = os.path.basename(npy_file).split('.')[0]
                    setattr(self, attribute_name, np.load(os.path.join(
                        class_path, npy_file))
                    )
                    pbar.update(1)
        else:
            for npy_file in files:
                attribute_name = os.path.basename(npy_file).split('.')[0]
                setattr(self, attribute_name, np.load(os.path.join(class_path,
                                                                   npy_file)))

    def _save_arrays(self):
        self.save_path = os.path.join(os.path.dirname(self.fort1_file_name),
                                      self.save_dir)
        attributes_to_delete = []
        for key in self.__dict__:
            if isinstance(self.__dict__[key], np.ndarray):
                npy_file_name = key + '.npy'
                np.save(os.path.join(self.save_path, npy_file_name),
                        self.__dict__[key])
                attributes_to_delete.append(key)

    def _delete_array_attributes(self):
        attributes_to_delete = []
        for key in self.__dict__:
            if isinstance(self.__dict__[key], np.ndarray):
                attributes_to_delete.append(key)
        for attribute in attributes_to_delete:
            delattr(self, attribute)

    def _save_class(self):
        self.save_path = os.path.join(os.path.dirname(self.fort1_file_name),
                                      self.save_dir)
        json_file = os.path.join(self.save_path, 'class.json')
        with open(json_file, 'w') as out_file:
            json.dump(self.__dict__, out_file)

    def _load_class(self, class_path):
        json_file = os.path.join(class_path, 'class.json')
        with open(json_file, 'r') as in_file:
            class_attributes = json.load(in_file)
            for key in class_attributes:
                setattr(self, key, class_attributes[key])
