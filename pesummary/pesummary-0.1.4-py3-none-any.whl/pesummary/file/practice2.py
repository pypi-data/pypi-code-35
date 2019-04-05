from six import iteritems
import h5py
import numpy as np

data = {"hello": {"my_name": {"is": {"not": [1,2,3]}, "this": {"nope": [1,2,3]}}}}

data = {
           "posterior_samples": {
                "H1_L1": {
                    "IMRPhenomPv2": {
                        "posterior_names": ["mass_1", "mass_2", "mass_3"],
                        "samples": [[1,2,3], [1,2,3], [1,2,3]]},
                    "IMRPhenomP": {
                        "posterior_names": ["mass_4", "mass_5", "mass_6"],
                        "samples": [[4,5,6], [4,5,6], [4,5,6]]
                    }
                },
                "H1": {
                    "IMRPhenomPv2": {
                        "posterior_names": ["mass_7", "mass_8", "mass_9"],
                        "samples": [[7,8,9], [7,8,9], [7,8,9]]},
                    "IMRPhenomP": {
                        "posterior_names": ["mass100", "mass200", "mass300"],
                        "samples": [[-1,-2,-3], [-4,-5,-6], [-7,-8,-9]]
                    }
                }
          
            }
        }

def paths_to_key(key, d, current_path=None):
    if current_path is None:
        current_path = []

    for k, v in d.items():
        if k == key:
            yield current_path + [key]
        else:
            if isinstance(v, dict):
                path = current_path + [k]
                yield from paths_to_key(key, v, path)

def _recursively_save_dictionary_to_hdf5_file(f, dictionary, current_path=None):
    """Recursively save a dictionary to a hdf5 file

    Parameters
    ----------
    f:
        opened h5py file
    dictionary: dict
        dictionary of data
    """
    try:
        f.create_group("posterior_samples")
    except:
        pass
    if current_path is None:
        current_path = []

    for k, v in dictionary.items():
        if isinstance(v, dict):
            try:
                f["/".join(current_path)].create_group(k)
            except:
                pass
            path = current_path + [k]
            _recursively_save_dictionary_to_hdf5_file(f, v, path)
        elif isinstance(v, list):
            if isinstance(v[0], str):
                f["/".join(current_path)].create_dataset(k, data=np.array(v, dtype="S"))
            elif isinstance(v[0], list):
                f["/".join(current_path)].create_dataset(k, data=np.array(v))

with h5py.File("hello.h5", "w") as f:
    _recursively_save_dictionary_to_hdf5_file(f, data)

