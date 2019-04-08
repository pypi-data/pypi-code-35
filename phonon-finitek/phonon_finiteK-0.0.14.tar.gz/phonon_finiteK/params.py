# -*- coding: utf-8 -*-
"""
Created on Sun Mar 11 11:05:28 2018

@author: Gabriele Coiana
"""

import numpy as np

import sys,os
#sys.path.append(os.getcwd()+'Phonons/Phonons/')

def get_parameters():
    """
    This function takes the input parameters from the file input.txt 
    and applies the right types to the variables
    """
    lista = []
    f = open('input', 'r')
    A = f.readlines()
    for string in A:
        index = string.find('=')+2
        lista.append(string[index:])
    
    latt = float(lista[1])
    
    
    m = lista[2]
    masses = np.fromstring(m, dtype=np.float, sep=',')
    mba,mti,mo = masses[0],masses[1],masses[2]
    
    N = lista[3]
    n = np.fromstring(N, dtype=np.int, sep=',')
    N1,N2,N3 = n[0],n[1],n[2]
    
    band = lista[4]
    a = np.fromstring(band, dtype=np.float, sep=',')
    num = len(a)/3
    ks = np.split(a,num)
    
    interp_wrong = lista[5]
    index = interp_wrong.find(' ')
    interp = interp_wrong[0:index]
    
    savefreq = int(lista[6])

     
    f.close()
    return latt, mba,mti,mo, N1,N2,N3, ks, interp, savefreq







