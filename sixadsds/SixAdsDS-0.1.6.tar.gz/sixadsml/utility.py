"""
Utility functions 
"""

import yaml
import numpy as np
from sqlalchemy import create_engine

def make_connection(specs):
    """
    Creates a connection based on the information in the *specs*. Ussually, 
    the *specs* dictionary is the output of the *read_yaml* function
    
    Parameters
    ----------
    
    **specs** : dictionary
        A dictionary that stores the user, password, host and db keys   
    
    Returns
    -------
    
        An sql_alchemy connection object    
    """
    engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
                       .format(user=specs['user'],
                               pw=specs['password'],
                               host = specs['host'],
                               db=specs['db']))
    return(engine)

def exec_file(file, add_params = None):
    """
    Executes a file with the .py extension
    
    Parameters
    ----------
    
    **file**: string
        path to the python file
        
   **add_params**:
        additional parameters that are used in the file that is beeing executed
    
    Returns
    -------
    
        Whatever output the executable file outputs    
    """
    if add_params is not None:
        exec(open(file).read(), add_params)
    else:
        exec(open(file).read())

def read_yaml(file):
    """
    Reads a .yml or .yaml file
    
    Parameters
    ----------
    
    **path**: string
    
        path to the .yml or .yaml files
    
    Returns
    -------
    
        Dictionary with the .yml or .yaml file contents 
    """
    with open(file, 'r') as f:
        d = yaml.load(f)
    
    return d    
        
def chunks_of_n(l, n):
    """
    Splits a list into n equal sizes
    
    Parameters
    ----------
    
    **l**: list
    
    **n**: int
    
    Returns
    -------
    
        A list of size *n* with the items of *l* splited equaly
    """
    list_chunked = []
    for i in range(0, len(l), n):
        list_chunked.append(l[i:i+n]) 
    
    return list_chunked    

def unique(l):
    """
    A handy function to return unique elements of a list or a numpy array
    
    Parameters
    ----------
    
    **l** : list or array
    
    Returns
    -------
    
        A list or array containing unique elements of l
    """
    
    l_unique = set(l)
    
    if isinstance(l, list):
        l_unique = list(l_unique)
    
    if isinstance(l, np.ndarray):
        l_unique = np.array(list(l_unique))    
    
    return l_unique
    
    
    
    
    