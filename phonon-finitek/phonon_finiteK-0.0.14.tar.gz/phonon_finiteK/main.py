#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 18:21:44 2018

@author: Gabriele Coiana
"""
import numpy as np

import sys,os
#sys.path.append(os.getcwd())

from phonon_finiteK import params
from phonon_finiteK import dynam
from phonon_finiteK import plot
from phonon_finiteK import bz
from phonon_finiteK import cell

# =============================================================================
# Parameters
a = params.get_parameters()[0]
mba, mti, mo = params.get_parameters()[1:4]
N1,N2,N3 = params.get_parameters()[4:7]
kinput = params.get_parameters()[7::][0]
interp = params.get_parameters()[8]
savefreq = params.get_parameters()[9]

N1N2N3 = N1*N2*N3 # Number of cells
N = N1*N2*N3*5    # Number of atoms
# =============================================================================
print('\nPho-NON-py')
print()
print('\nCalculating the k points...')
ks, ks_scaled, kk = bz.getk(a,N1,N2,N3,kinput)
print('Ok baby, Im gonna take all of these kpoints (scaled):\n',ks_scaled)


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
























