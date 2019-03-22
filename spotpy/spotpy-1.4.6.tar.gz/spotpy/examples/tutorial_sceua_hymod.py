# -*- coding: utf-8 -*-
'''
Copyright 2015 by Tobias Houska
This file is part of Statistical Parameter Estimation Tool (SPOTPY).

:author: Tobias Houska

This class holds example code how to use the dream algorithm
'''

import numpy as np
import spotpy
from spotpy.examples.spot_setup_hymod_python import spot_setup
import pylab as plt

#import h5py
#import pandas as pd

if __name__ == "__main__":
    parallel ='seq' # Runs everthing in sequential mode
    np.random.seed(2000) # Makes the results reproduceable
    
    # Initialize the Hymod example
    # In this case, we tell the setup which algorithm we want to use, so
    # we can use this exmaple for different algorithms
    spot_setup=spot_setup(_used_algorithm='sceua')
    
    #Select number of maximum allowed repetitions
    rep=10000
    filename = 'SCEUA_hymod'
    # Create the SCE-UA sampler of spotpy, alt_objfun is set to None to force SPOTPY
    # to jump into the def objectivefunction in the spot_setup class (default is
    # spotpy.objectivefunctions.rmse) 
    sampler=spotpy.algorithms.sceua(spot_setup, dbname='SCEUA_hymod', dbformat='csv', alt_objfun=None)
    
    #Start the sampler, one can specify ngs, kstop, peps and pcento id desired
    sampler.sample(rep) 
    
    # Load the results gained with the sceua sampler, stored in SCEUA_hymod.csv
    #results = spotpy.analyser.load_hdf5_results('SCEUA_hymod')
    results = spotpy.analyser.load_csv_results('SCEUA_hymod')
    

    print(len(results))
    # Store "x" in a chunked array...
#    f = tables.openFile('SCEUA_hymod.h5', 'r')
#    atom = tables.Atom.from_dtype(x.dtype)
#    ds = f.createCArray(f.root, 'somename', atom, x.shape)
#    ds[:] = x
#    f.close()
#    with h5py.File('SCEUA_hymod.h5', 'r') as f:
#        my_array = f['SCEUA_hymod'][()]
#
#    import pandas as pd
#    a=pd.read_hdf('SCEUA_hymod.h5','SCEUA_hymod')
    
#    import h5py
#
#    f = h5py.File('SCEUA_hymod.h5')['SCEUA_hymod']
#
#    import operator
#    from functools import reduce
#    reduce(operator.concat, f)

    #print(list(f))
#    all_other = list(my_array.dtype.names[0:-2])
#    #all_other.append(my_array.dtype.names[-1])
#    
#    simulations = my_array[my_array.dtype.names[-2]]
#
##    header=[]
##    for i in range(len(simulations)):
##        if isinstance(simulations[0], list) or type(simulations[0]) == type(np.array([])):
##            for j in range(len(simulations[i])):
##                header.append(tuple(('simulation' + str(i+1)+'_'+str(j+1), '<f8')))
#
#    header=[]
#    for i in range(len(simulations[0])):
#        #header.append(('simulation1'+'_'+str(i+1)))
#        header.append(tuple(('simulation1_'+str(i+1), '<f8')))
#        
#    new_header = all_other+header+[my_array.dtype.names[-1]]
#    
#    new_header
    
    
    #db = tables.open_file('SCEUA_hymod'+'.h5')
#    file    = h5py.File('SCEUA_hymod.h5', 'r')   # 'r' means that hdf5 file is open in read-only mode
#    dataset = file[dataset_name]
#    arr1ev  = dataset[event_number]
#    file.close()
#    
    fig= plt.figure(1,figsize=(9,5))
    plt.plot(results['like1'])
    plt.show()
    plt.ylabel('RMSE')
    plt.xlabel('Iteration')
    fig.savefig('hymod_objectivefunction.png',dpi=300)
    
    # Example plot to show the parameter distribution ###### 
    fig= plt.figure(2,figsize=(9,9))
    normed_value = 1
    
    plt.subplot(5,2,1)
    x = results['parcmax']
    for i in range(int(max(results['chain'])-1)):
        index=np.where(results['chain']==i+1) #Ignores burn-in chain
        plt.plot(x[index],'.')
    plt.ylabel('cmax')
    plt.ylim(spot_setup.cmax.minbound, spot_setup.cmax.maxbound)
    
    
    plt.subplot(5,2,2)
    x = x[int(len(results)*0.9):] #choose the last 10% of the sample
    hist, bins = np.histogram(x, bins=20, density=True)
    widths = np.diff(bins)
    hist *= normed_value
    plt.bar(bins[:-1], hist, widths)
    plt.ylabel('cmax')
    plt.xlim(spot_setup.cmax.minbound, spot_setup.cmax.maxbound)
    
    
    plt.subplot(5,2,3)
    x = results['parbexp']
    for i in range(int(max(results['chain'])-1)):
        index=np.where(results['chain']==i+1)
        plt.plot(x[index],'.')
    plt.ylabel('bexp')
    plt.ylim(spot_setup.bexp.minbound, spot_setup.bexp.maxbound)
    
    plt.subplot(5,2,4)
    x = x[int(len(results)*0.9):]
    hist, bins = np.histogram(x, bins=20, density=True)
    widths = np.diff(bins)
    hist *= normed_value
    plt.bar(bins[:-1], hist, widths)
    plt.ylabel('bexp')
    plt.xlim(spot_setup.bexp.minbound, spot_setup.bexp.maxbound)
    
    
    
    plt.subplot(5,2,5)
    x = results['paralpha']
    for i in range(int(max(results['chain'])-1)):
        index=np.where(results['chain']==i+1)
        plt.plot(x[index],'.')
    plt.ylabel('alpha')
    plt.ylim(spot_setup.alpha.minbound, spot_setup.alpha.maxbound)
    
    
    plt.subplot(5,2,6)
    x = x[int(len(results)*0.9):]
    hist, bins = np.histogram(x, bins=20, density=True)
    widths = np.diff(bins)
    hist *= normed_value
    plt.bar(bins[:-1], hist, widths)
    plt.ylabel('alpha')
    plt.xlim(spot_setup.alpha.minbound, spot_setup.alpha.maxbound)
    
    
    plt.subplot(5,2,7)
    x = results['parKs']
    for i in range(int(max(results['chain'])-1)):
        index=np.where(results['chain']==i+1)
        plt.plot(x[index],'.')
    plt.ylabel('Ks')
    plt.ylim(spot_setup.Ks.minbound, spot_setup.Ks.maxbound)
    
    
    plt.subplot(5,2,8)
    x = x[int(len(results)*0.9):]

    hist, bins = np.histogram(x, bins=20, density=True)
    widths = np.diff(bins)
    hist *= normed_value
    plt.bar(bins[:-1], hist, widths)
    plt.ylabel('Ks')
    plt.xlim(spot_setup.Ks.minbound, spot_setup.Ks.maxbound)
    
    
    plt.subplot(5,2,9)
    x = results['parKq']
    for i in range(int(max(results['chain'])-1)):
        index=np.where(results['chain']==i+1)
        plt.plot(x[index],'.')
    plt.ylabel('Kq')
    plt.ylim(spot_setup.Kq.minbound, spot_setup.Kq.maxbound)
    plt.xlabel('Iterations')
    
    plt.subplot(5,2,10)
    x = x[int(len(results)*0.9):]
    hist, bins = np.histogram(x, bins=20, density=True)
    widths = np.diff(bins)
    hist *= normed_value
    plt.bar(bins[:-1], hist, widths)
    plt.ylabel('Kq')
    plt.xlabel('Parameter range')
    plt.xlim(spot_setup.Kq.minbound, spot_setup.Kq.maxbound)
    plt.show()
    fig.savefig('hymod_parameters.png',dpi=300)