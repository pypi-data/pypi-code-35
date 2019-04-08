# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 10:09:19 2019

@author: Gabriele Coiana
"""

import numpy as np

#def partition(omegas,T):
#    hbar = 1 #atomic units
#    kb = 3.1668085639379e-06 #atomic units
#    c = 0.0001519828500716 #Thz to Hartree
#    
#    
#    a = 1/(1-np.exp(-hbar*omegas/(kb*T)))
#    Z = np.prod(a)
#    return Z
#
#
#def free_energy2(omegas,Ts):
#    hbar = 1 #atomic units
#    kb = 3.1668085639379e-06 #atomic units
#    c = 0.0001519828500716 #Thz to Hartree
#    omegas = c*omegas*2*np.pi
#    F = []
#    for t in Ts:
#        print(np.log(partition(omegas,t)))
#        F.append(-kb*t*np.log(partition(omegas,t)))
#    F = np.array(F)
#    return F*627.509





















def bose_einstein(omegas,Ts):
    hbar = 1 #atomic units
    kb = 3.1668085639379e-06 #atomic units
    c = 0.0001519828500716 #Thz to Hartree
    omegas = c*omegas
    
    nk = 1/(np.exp(np.multiply(hbar*omegas,1/(kb*Ts.T))) - 1)
    n = np.sum(nk,axis=0)
    return n

def nk(omega,T):
    hbar = 1 #atomic units
    kb = 1#3.1668085639379e-06 #atomic units
    c = 0.16
    n = (np.exp(c*hbar*omega/(kb*T))-1)**(-1)
    return n


def free_energy(freqs,Ts):
    hbar = 1 #atomic units
    #kb = 3.1668085639379e-06 #atomic units
    c = 6.62607015*6.022*10/1000 #conversion frequency to kJ/mol
    
    F0 = []
    for temp in Ts:
        a = -kb*temp*(np.sum(np.log(nk(freqs,temp))))
        F0.append((0.5*np.sum(hbar*freqs)+a))
    F0 = np.array(F0)
#    n = bose_einstein(omegas,Ts)
#    F = 0.5*np.sum(hbar*omegas)-kb*np.multiply(Ts,np.log(n))
    return F0*c

def entropy(freqs,Ts,dT):
    F = free_energy(freqs,Ts) 
    S = -np.gradient(F,dT)
    return S*1000 #conversion to J/K/mol

def energy(freqs,Ts):
    hbar = 1 #atomic units
    #kb = 3.1668085639379e-06 #atomic units
    c = 6.62607015*6.022*10/1000 #conversion frequency to kJ/mol
    E0 = []
    for temp in Ts:
        #print(temp, nk(omegas,temp))
        #E0.append(float(np.real(np.dot(hbar*omegas.T,0.5+nk(omegas,temp)))))
        E0 = 0.5*np.sum(freqs) 
    E0 = np.array(E0)   
#    a = np.real((np.exp(hbar*np.dot(omegas,1/(kb*Ts.T)))-1)**(-1)+0.5)
#    E = np.dot(omegas.T,a).T
#    E = E.reshape(np.size(E))
    return E0*c

def cv(freqs,Ts,dT):
    E = energy(freqs,Ts)
    cv = np.gradient(E,dT)
    return cv*1000 #conversion to J/K/mol

## =============================================================================
## Parameters
#a = params.get_parameters()[0]
#mba, mti, mo = params.get_parameters()[1:4]
#N1,N2,N3 = params.get_parameters()[4:7]
#kinput = params.get_parameters()[7::][0]
#interp = params.get_parameters()[8]
#savefreq = params.get_parameters()[9]
#therm = params.get_parameters()[10]
#
#N1N2N3 = N1*N2*N3 # Number of cells
#N = N1*N2*N3*5    # Number of atoms
# =============================================================================
#omegas = np.array([1,2,3])
#omegas = omegas.reshape(len(omegas),1)
#Ts = np.arange(1,101)
#Ts = Ts.reshape(len(Ts),1)
#E = energy(omegas,Ts)
#print(E)