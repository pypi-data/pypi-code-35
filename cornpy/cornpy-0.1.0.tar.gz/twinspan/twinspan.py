import os
from ..utils import write_cep

def twinspan(data, cut_levels=-1, min_group_size=-1, levels=-1, diagrams=-1):
    """
    Two-Way INdicator SPecies ANalysis.
    
    This function computes the two-way indicator species analysis classification
    algorithm. It is a Python wrapper around the program TWINSPAN written in 
    Fortran by M.O. Hill (1979).
    
    Parameters
    ----------
    data : dataframe
        A pandas dataframe
    cut_levels : list
        Pseudospecies cut levels (default = [0,2,5,10,20]). Should not exceed 
        9 cut levels
    min_group_size : int	
        Minimum size of the group, which should not be further divided 
        (default = 5)
    levels : int
        Number of hierarchical levels of divisions (default = 6, should be 
        between 0 and 15)    
        
    Returns
    -------
    output : str
        Two-way classification table
        
    Example
    -------
    import pandas as pd
    import cornpy as cp
    df = pd.read_csv("data.csv")
    output = twinspan(df)
    """ 
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    
    nrows, ncols = write_cep(data)
    
    with open("params.dat", 'w') as parfile:
        parfile.write("cep.dat\n")
        parfile.write("%s\n" % -1)
        parfile.write("%s\n" % cut_levels)
        parfile.write("%s\n" % min_group_size)
        parfile.write("%s\n" % -1)
        parfile.write("%s\n" % -1)
        parfile.write("%s\n" % levels)
        parfile.write("%s\n" % -1)
        parfile.write("%s\n" % -1)
        parfile.write("%s\n" % -1)
        parfile.write("%s\n" % -1)
        parfile.write("%s\n" % -1)
    
    output = os.popen("twinspan < params.dat").read()
    
    os.remove("cep.dat")
    os.remove("params.dat")
    
    with open("twinspan.prt", 'r') as f:
        output = f.read()
    
    os.remove("twinspan.prt")
    
    pos = output.find(chr(12))
    results = output[pos:].strip()
    cut_levels = [0,2,5,10,20] if cut_levels == -1 else cut_levels
    min_group_size = 5 if min_group_size == -1 else min_group_size
    levels = 6 if levels == -1 else levels
    print('Standard TWINSPAN (Hill 1979)\n')
    print('Basic setting:')
    print('Pseudospecies cut levels: ', ' '.join(str(n) for n in cut_levels))
    print('Minimum group size: ', str(min_group_size))
    print('Number of hierarchical levels: ', str(levels))
    return results[1:]