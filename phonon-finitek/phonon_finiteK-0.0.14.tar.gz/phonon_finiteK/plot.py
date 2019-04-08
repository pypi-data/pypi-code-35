#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 16:00:25 2018

@author: Gabriele Coiana
"""
import numpy as np
from scipy.interpolate import interp1d

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation

def transf_frequencies(frequencies):
    freq = np.copy(frequencies)
    for i in range(len(freq)):
        for j in range(len(freq[0])):
            if (np.abs(np.imag(freq[i,j])) <= 5):
                freq[i,j] = np.real(frequencies[i,j])
            else:
                freq[i,j] = - np.abs(np.imag(frequencies[i,j]))       
    return freq 

def interp(kk,frequencies, index_0_withboundaries, method='linear'):
    acou = []
    optic = []
    index_acou = []
    freq = transf_frequencies(frequencies)
    
    for i in range(len(frequencies)):
        for j in range(len(frequencies[0])):
            if(np.abs(np.real(frequencies[i,j])) <= 0.01 and np.abs(np.imag(frequencies[i,j])) <= 0.01):
                index_acou.append(i)

    for i in index_acou:
        for j in range(len(index_0_withboundaries)-1):
            acou.append(interp1d(kk[index_0_withboundaries[j]:index_0_withboundaries[j+1]+1],frequencies[i,index_0_withboundaries[j]:index_0_withboundaries[j+1]+1],method))
            
    for i in range(len(frequencies)):
        if(i in index_acou):
            continue
        optic.append(interp1d(kk,freq[i,:],method))
        
    return index_acou, acou, optic

def plot(ks, kk, frequencies, interpol):
    fig,ax = plt.subplots()
    index_0 = []
    for i in range(len(ks)):
        if np.array_equal(ks[i],[0.,0.,0.]):
            index_0.append(i)
    
    index_0_withboundaries = index_0     
    if(index_0[-1] != len(kk)-1):
        index_0_withboundaries.append(len(kk)-1)
        
    if(index_0[0] != 0):
        index_0_withboundaries.insert(0,0)
    
    freq = transf_frequencies(frequencies)
    
    for i in range(len(frequencies)):
        ax.scatter(kk,freq[i,:],marker='o')
    
    
    if(interpol in ['cubic','quadratic','linear']):
        index_acou, acou, optic = interp(kk, frequencies, index_0_withboundaries, method=interpol)
        for i in range(len(index_acou)):
            for j in range(len(index_0_withboundaries)-1):
                xj = np.arange(kk[index_0_withboundaries[j]],kk[index_0_withboundaries[j+1]],0.01)
                ax.plot(xj,acou[i*(len(index_0_withboundaries)-1)+j](xj),c='r')
                
        x = np.arange(kk[0],kk[-1],0.01)
        for i in range(len(frequencies)-3):
            ax.plot(x,optic[i](x),c='r')
    
    
    Points = {'$\Gamma$':[0,0,0],'X':[0.5,0,0],'M':[0.5,0.5,0],'R':[0.5,0.5,0.5],'boh':[0,0.5,0], 'Z':[0,0,0.5]}
    x_labels = []
    for kpoint in ks:
        a = 0
        for element in Points.items():
            a = a + 1
            if (np.array_equal(kpoint , element[1])):
                x_labels.append(element[0])
                break
            if (a==len(Points.items())):
                x_labels.append(' ')
    
    ax.set_xlabel('Wave vector')
    ax.set_ylabel('Frequency [Thz]')           
    plt.xticks(kk,x_labels)
    ax.axhline(0, linestyle='--', color='b')
    plt.grid(axis='y')
    plt.show()
    fig.savefig('dispersion.pdf')
    return




