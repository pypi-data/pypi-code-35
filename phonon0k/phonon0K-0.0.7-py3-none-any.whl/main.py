#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 18:21:44 2018

@author: Gabriele Coiana
"""
import numpy as np

import sys,os
#sys.path.append(os.getcwd())

from phonon import params
from phonon import dynam
from phonon import plot
from phonon import bz
from phonon import cell
from phonon import thermal

# =============================================================================
# Parameters
a = params.get_parameters()[0]
mba, mti, mo = params.get_parameters()[1:4]
N1,N2,N3 = params.get_parameters()[4:7]
kinput = params.get_parameters()[7::][0]
interp = params.get_parameters()[8]
savefreq = params.get_parameters()[9]
therm = params.get_parameters()[10]

N1N2N3 = N1*N2*N3 # Number of cells
N = N1*N2*N3*5    # Number of atoms
# =============================================================================

#if (__name__ == "__main__"):
print('\nPho-NON-py')
print()
print('\nCalculating the k points...')
ks, ks_scaled, kk, allks = bz.getk(a,N1,N2,N3,kinput)
print('Ok babe, Im gonna take all of these kpoints (scaled):\n',ks_scaled)


print('\nComputing the stiffness matrix...')
K = dynam.K(N1N2N3)
print('\tK is equilibrated to within ',np.max(np.abs(np.sum(K,axis=1))))

print('\nCalculating dynamical matrixes...')
FREQ = []
mode = str(sys.argv[1])
for kpoint in ks:
    D = dynam.D(kpoint,K,N1,N2,N3,mba,mti,mo,mode)
    
    ll = np.matrix(D)
    print('\t',str(kpoint),' Hermitian: ',np.allclose(ll,ll.getH(),rtol=0.01,atol=0.01))
    
    eigvals, eigvec = np.linalg.eig(D)
    idx = eigvals.argsort()[::-1]   
    eigvals = eigvals[idx]  
    eigvec = eigvec[:,idx]
    freq = (np.sqrt(eigvals)/(2*np.pi))
    FREQ.append(freq)
print()


FREQ = np.array(FREQ).T

if(savefreq):
    np.savetxt('frequencies',np.column_stack([FREQ.real, FREQ.imag]))
    np.savetxt('frequencies_niceview',FREQ, fmt='%-1.2d')



plot.plot(ks_scaled,kk, FREQ,interp)


if (therm):
    ks, ks_scaled, kk, allks = bz.getk(a,N1,N2,N3,kinput)
    FREQ = []
    print(np.shape(allks))
    for kpoint in allks:
        print(kpoint)
        D = dynam.D(kpoint,K,N1,N2,N3,mba,mti,mo,mode)
        
        eigvals, eigvec = np.linalg.eig(D)
        idx = eigvals.argsort()[::-1]   
        eigvals = eigvals[idx]  
        eigvec = eigvec[:,idx]
        freq = (np.sqrt(eigvals)/(2*np.pi))
        FREQ.append(freq)
    FREQ = np.array(FREQ)
    
    freq = FREQ.reshape((np.size(FREQ),1))
    
    c = 6.626*6.022*1e+01
    c1 = 0.3990
    #print(.5*np.sum(freq)*c1/N)
    
    dT = 10
    T = np.arange(10,1000,dT)
    
    F = thermal.free_energy(freq,T)/N
    S = thermal.entropy(freq,T,dT)
    
    dulong_petite = 3*N*1.38064852*1e-23
    T = T.reshape(len(T),1)
    E = thermal.energy(freq,T)/N
    print(E)
    
    
    
    
    
    cv = thermal.cv(freq,T,dT)
    
    #plot.plot_thermal(T,E,F,S,cv)
    
    





















