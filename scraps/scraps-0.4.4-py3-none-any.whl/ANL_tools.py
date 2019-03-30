import os

import numpy as np
import pandas as pd
import glob

try: import simplejson as json
except ImportError: import json

from .process_file import process_file

def find_nearest(x, array):
    """Return the value of array that is closest to the value of x"""
    ix = np.abs(array-x).argmin()
    return array[ix]

def build_metadf(basepath, meta_style='json'):
    """Build a metadata DataFrame from a directory full of resonator files.

    Paramaters
    ----------
    basepath: string
        Path to the directory containing the data

    meta_style: string
        Type of metadata. Can be 'filename' or 'json'
    
    Return
    ------
    temperature_index : numpy.array
        An index of unique temperature values."""

    metadf = pd.DataFrame(columns=['Temperature', 'Power', 'Name'])

    for ix, filename in enumerate(glob.glob(os.path.join(basepath, '*.S2P'))):
        
        if meta_style == 'json':
            with open(filename, 'r') as f:
                metadata = json.loads(f.readline())
            
            power = float(metadata['input_power'])-float(metadata['internal_atten'])-float(metadata['var_atten'])
            temperature = metadata['temp']
            name = metadata['res_name']

        elif meta_style == 'filename':
            metadata = process_file(filename, meta_only=True)
            power = metadata['pwr']
            temperature = metadata['temp']
            name = metadata['name']
        
        metadf.loc[ix] = [temperature, power, name]

    return metadf

def pivot_metadf_temp(metadf):
    """Pivots the metadf to put temperature as the value. Useful for debugging."""
    grp_metadf = metadf.groupby(['Name', 'Power'])
    length = max(len(v) for k, v in grp_metadf)
    newdf = pd.DataFrame()
    for k, v in metadf.groupby(['Name', 'Power']):
        newdf[k] = np.pad(v.sort_values(by='Temperature')['Temperature'].values,
                          (0,length-len(v)),
                          mode='constant',
                          constant_values=np.NaN)

    return newdf

def get_temperature_index(metadf):
    """Get a temperature index from metadata DataFrame returned by
    build_metadf."""

    num_powers = len(metadf['Power'].unique())
    num_res = len(metadf['Name'].unique())

    #Non-identical values, so have to infer
    num_temps = int(len(metadf)/(num_powers*num_res))

    datacube_shape = (num_powers,
                    num_temps,
                    num_res)

    temperature_index = (np.reshape(metadf.sort_values(by=['Power', 'Temperature'])['Temperature'].values, datacube_shape)
                    .mean(axis=0) #Average along powers
                    .mean(axis=1) #Average along resonators
                    *1000).astype(int)/1000 #Round to nearest mK

    return temperature_index