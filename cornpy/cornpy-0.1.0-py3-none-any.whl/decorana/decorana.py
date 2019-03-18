import os
import numpy as np
from ..utils import write_cep

def decorana(data, iweigh=0, iresc=0, ira=0, mk=0, short=0):
    """
    Detrended correspondence analysis and basic reciprocal averaging.
    
    This function performs detrended correspondence analysis and basic 
    reciprocal averaging or orthogonal correspondence analysis. It is a
    Python wrapper around the program DECORANA written in Fortran by 
    M.O. Hill (1979). 
    
    Parameters
    ----------
    data : dataframe
        A pandas dataframe
    iweigh : int
        Downweighting of rare species (default = 0: no)
    iresc : int
        Number of rescaling cycles (default = 0: no rescaling)
    ira	: int
        Type of analysis (0: detrended, 1: basic reciprocal averaging, 
        default = 0)
    mk : int	
        Number of segments in rescaling (default = 0)
    short : int
        Shortest gradient to be rescaled (default = 0)
    
    Returns
    -------
    site_scores : array
        array of site scores
    species_scores : array
        array of species scores
        
    Example
    -------
    import pandas as pd
    import cornpy as cp
    df = pd.read_csv("data.csv")
    site_scores, species_scores = cp.decorana(df)
    """ 
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
   
    nrows, ncols = write_cep(data)
    
    with open("params.dat", 'w') as parfile:
        parfile.write("cep.dat\n")
        parfile.write("%s " % -1)
        parfile.write("%s\n" % 0)
        parfile.write("%s\n" % iweigh)
        parfile.write("%s\n" % iresc)
        parfile.write("%s\n" % ira)
        parfile.write("%s\n" % mk)
        parfile.write("%s\n" % short)
        parfile.write("%s\n" % 1)
        parfile.write("%s\n" % 0)
    
    output = os.popen("decorana < params.dat").read()
    
    os.remove("cep.dat")
    os.remove("params.dat")
    
    site_scores = np.genfromtxt("decorana.out", usecols=(0,1,2,3), max_rows=nrows)
    species_scores = np.genfromtxt([s[41:] for s in open("decorana.out")], usecols=(0,1,2,3), max_rows=ncols)
    
    os.remove("decorana.out")
    os.remove("decorana.prt")
    
    return site_scores, species_scores