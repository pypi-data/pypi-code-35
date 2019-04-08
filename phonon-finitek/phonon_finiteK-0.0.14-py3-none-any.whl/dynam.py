#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 14:03:17 2018

@author: Gabriele Coiana
"""

import numpy as np
import os

from phonon_finiteK import bz
from phonon_finiteK import cell
from phonon_finiteK import params



def K(N1N2N3):
    """
    Builds the stiffness matrix
    """
    N = N1N2N3*5
    K = np.zeros((15,N*3))
    with open('FORCE_SETS','r') as f:
        A = f.readlines()
    
    i = 0
    for l,i,m in zip(range(5,(3+N)*15*2,3+N),np.repeat(np.arange(15),2),np.tile((0.001*0.5292,-0.001*0.5292),15)):
        
        B = A[l:l+N]
        with open('try','w') as g:
            g.writelines(B)
        C = np.loadtxt('try')
        D = C.reshape(1,N*3)
        
        K[i,:] = K[i,:] + D/m
    os.remove('try')  
    return -K/2

def R_matrix(N1,N2,N3,mode):
    """
    returns the R matrix
    """
    N1N2N3 = N1 * N2 * N3
    N = N1N2N3*5
        
    if(mode=='cubic'):
        bati = cell.BaTiO3(4)
        bati.supercell(N1,N2,N3)
        Rba = bati.Ba.reshape(1,N1N2N3*3) 
        Rti = bati.Ti.reshape(1,N1N2N3*3) 
        Ro1 = bati.O1.reshape(1,N1N2N3*3) 
        Ro2 = bati.O2.reshape(1,N1N2N3*3) 
        Ro3 = bati.O3.reshape(1,N1N2N3*3)
        
        Ractual = np.hstack((Rba,Rti,Ro1,Ro2,Ro3))
        
        R0 = Ractual - np.tile(Ractual[0,0:0+3],N)
        R0 = np.repeat(R0,3,axis=0)
        R1 = Ractual - np.tile(Ractual[0,3*N1N2N3:3*N1N2N3+3],N)
        R1 = np.repeat(R1,3,axis=0)
        R2 = Ractual - np.tile(Ractual[0,3*N1N2N3*2:3*N1N2N3*2+3],N)
        R2 = np.repeat(R2,3,axis=0)
        R3 = Ractual - np.tile(Ractual[0,3*N1N2N3*3:3*N1N2N3*3+3],N)
        R3 = np.repeat(R3,3,axis=0)
        R4 = Ractual - np.tile(Ractual[0,3*N1N2N3*4:3*N1N2N3*4+3],N)
        R4 = np.repeat(R4,3,axis=0)
        R = np.vstack((R0,R1,R2,R3,R4))
        
    else:
        Rall = np.loadtxt('../../NPE/pos',usecols=(1,2,3))
        Rall = Rall - Rall[0,:]
        R = np.zeros((N,3))
        n = 0
        for i in range(0,len(Rall),N):
            n = n + 1
            pos_cm = np.sum(Rall[i:i+N,:],axis=0)/N
            Rall[i:i+N] = Rall[i:i+N] - pos_cm
            R = R + Rall[i:i+N]
        Ravg = R/n

        Ractual = Ravg.reshape(1,N*3)
        R0 = Ractual - np.tile(Ractual[0,0:0+3],N)
        R0 = np.repeat(R0,3,axis=0)
        R1 = Ractual - np.tile(Ractual[0,3*N1N2N3:3*N1N2N3+3],N)
        R1 = np.repeat(R1,3,axis=0)
        R2 = Ractual - np.tile(Ractual[0,3*N1N2N3*2:3*N1N2N3*2+3],N)
        R2 = np.repeat(R2,3,axis=0)
        R3 = Ractual - np.tile(Ractual[0,3*N1N2N3*3:3*N1N2N3*3+3],N)
        R3 = np.repeat(R3,3,axis=0)
        R4 = Ractual - np.tile(Ractual[0,3*N1N2N3*4:3*N1N2N3*4+3],N)
        R4 = np.repeat(R4,3,axis=0)
        R = np.vstack((R0,R1,R2,R3,R4))
        
    return R#*0.529177249







def D(k, K,N1,N2,N3,mba, mti, mo, mode):
    """
    builds the dynamical matrix
    """
    N1N2N3 = N1 * N2 * N3
    N = N1N2N3*5
    m = np.array([mba,mba,mba,mti,mti,mti,mo,mo,mo,mo,mo,mo,mo,mo,mo])
           
    #prepare kdotr
    R = R_matrix(N1,N2,N3,mode)
    kdotr = np.zeros((15,N*3))
    for i in range(15):
        for j in range(0,N*3,3):
            kdotr[i,j] = np.dot(k,R[i,j:j+3])
            kdotr[i,j+1] = np.dot(k,R[i,j:j+3])
            kdotr[i,j+2] = np.dot(k,R[i,j:j+3])
    
    D = np.zeros((15,15),dtype=complex)
    for i in range(15):
        for j,h in zip(range(15),np.repeat(range(0,N),3)):
            mass_coeff = complex(1/(m[i]*m[j])**(0.5))
            exp = 0*1j
            #h = 0
            for l in range(j+h*3*(N1N2N3-1),j+h*3*(N1N2N3-1)+(N1N2N3)*3,3):
                #print(l)
                #print(np.exp(1j*kdotr[i,l]),K[i,l])
                exp = exp + K[i,l]*np.exp(1j*kdotr[i,l])
            #print()
            D[i,j] = mass_coeff*exp
    return D*0.964*10**(4)#, kdotr, R



## =============================================================================
## Parameters
#a = params.get_parameters()[0]
#mba, mti, mo = params.get_parameters()[1:4]
#N1,N2,N3 = params.get_parameters()[4:7]
#kinput = params.get_parameters()[7::][0]
#interp = params.get_parameters()[8]
#savefreq = params.get_parameters()[9]
#
#N1N2N3 = N1*N2*N3 # Number of cells
#N = N1*N2*N3*5    # Number of atoms
## =============================================================================










