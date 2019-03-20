#!/usr/bin/env python

# built-in libraries
from copy import deepcopy
import time
import os
# external libraries
import numpy as np
import pandas as pd
# my files
from bd_resample import *
from reg_bd_svd import *
from reg_bd3 import *

def bdreg_v1(B,N=None,VamModel=None,BuildModel=None):
    print('## bdreg.py')
    start = time.time()
    np.set_printoptions(precision=5,suppress=True)

    if N == None:
        N=50

    if not BuildModel:
        print('applying model')
        N = VamModel['N']
    elif BuildModel:
        print('building model')
        VamModel['N']= N

    plotres=0
    bnreg0=deepcopy(B)
    kll=len(B)
    bdpc=np.zeros([kll,2*N])
    bdpc0=deepcopy(bdpc)
    sc=np.zeros([kll,1])

    for ktt in range(kll): # speed : 3 sec
        bdt=bd_resample((B.loc[ktt]),N)
        B.loc[ktt],sc[ktt]=reg_bd_svd(bdt)
        bdpc0[ktt]=np.append([B[ktt][1]],[B[ktt][0]],axis=1)
    mbdpc0 = [sum(x)/len(x) for x in zip(*bdpc0)]
    bdr0=np.append([mbdpc0[N:]],[mbdpc0[0:N]],axis=0)

    if BuildModel:
        bdrn=deepcopy(bdr0)
        VamModel['bdrn']=bdrn
    else:
        bdrn=VamModel['bdrn']

    outyt=np.zeros([kll,1])
    bnreg=deepcopy(B)

    for ktt in range(kll): # speed : 60 sec
        bnreg[ktt],outyt[ktt]=reg_bd3(bnreg.loc[ktt],bdrn)
        bdpc[ktt]=np.append(bnreg[ktt][1],bnreg[ktt][0])

    return bdpc, bnreg, sc, VamModel

def bdreg_main(df,N=None,VamModel=None,BuildModel=None):
    start = time.time() #record time
    bdpc, bnreg, sc, VamModel=bdreg_v1(df[0],N,VamModel,BuildModel)
    end = time.time()
    print('For bdreg, elapsed time is ' + str(end-start) + 'seconds...')
    return bdpc, bnreg, sc, VamModel


