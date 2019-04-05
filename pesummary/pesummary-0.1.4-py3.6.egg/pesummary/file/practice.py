import h5py
from meta_file import _recursively_save_dictionary_to_hdf5_file


data = {"posterior_samples": {
            "H1_L1": {
                "IMRPhenomPv2": {
                    "parameter_names": ["mass_1", "mass_2", "phiJL"],
                    "samples": [1.0, 2.0, 3.0]
                },
                "IMRPhenomP": {
                    "parameter_names": ["luminosity_distance", "ra"],
                    "samples": [10, 5]
                }
            }
        }
}

with h5py.File("hello.h5", "w") as f:
    _recursively_save_dictionary_to_hdf5_file(f, data)
