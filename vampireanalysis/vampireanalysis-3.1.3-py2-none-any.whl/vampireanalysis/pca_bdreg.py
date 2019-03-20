#!/usr/bin/env python

# built-in libraries
from __future__ import division
from copy import deepcopy
import time
# external libraries
import numpy as np
import pandas as pd
import matplotlib as mpl
mpl.use("TkAgg")
import matplotlib.pyplot as plt
# my files
from PCA import *

def pca_bdreg_v1(bdpc,VamModel,BuildModel,ch):
    print('## pca_bdreg.py')
    np.set_printoptions(precision=5,suppress=True)

    Nuu = int(round(len(bdpc.T[0])))
    Nbb = int(round(len(bdpc[0])/2))
    pcnum0 = 12
    dstp = 3
    bdpct = deepcopy(bdpc)

    if BuildModel:
        mmx = np.ones((Nuu,1)) * np.mean(bdpct,axis=0)
    else: 
        mmx = np.ones((Nuu,1)) * VamModel['mdd']   
    smx = np.ones(bdpct.shape)
    test = np.divide((bdpct-mmx),smx)
    if BuildModel:
        pc,score,latent=PCA(test)
        score = np.dot(test,pc)
    else: 
        latent = VamModel['latent']
        pc = VamModel['pc']
        score = np.dot(test,pc)

    mdd = mmx[0]
    sdd = smx[0]
    mss = np.mean(score,axis=0) 
    sss = np.std(score,axis=0) 
    cnum = 1

    ce1 = score[cnum-1] 

    xr = bdpct[cnum-1][0:Nbb]
    yr = bdpct[cnum-1][Nbb:]

    VamModel['mdd']=mdd
    VamModel['sdd']=sdd
    VamModel['pc']=pc
    VamModel['latent']=latent

    plt.figure(1)
    plt.clf()

    #check I: check the shape of principle component; 
    if True:
        plt.figure(221)
        plt.clf()
        for pcnum in range(10):
            dxx = 0.7
            xx = pc.T[pcnum][0:Nbb]
            yy = pc.T[pcnum][Nbb:]
            plt.plot(xx+(pcnum+1)*dxx,yy,'b-',linewidth=2.0)
            plt.plot(-xx+(pcnum+1)*dxx,-yy-dxx,'r-',linewidth=2.0)
        plt.axis('equal')
        plt.axis('off')


    #check II: the mean +- std of PC mean
    if True:
        cmap = plt.cm.jet
        vmax = int(11)
        norm = mpl.colors.Normalize(vmin=0,vmax=vmax)
        cid = plt.cm.ScalarMappable(norm=norm,cmap=cmap)

        offx,offy=np.meshgrid(range(pcnum0),[0])
        offx=np.multiply((offx+1),dstp)[0]
        offy=np.multiply(-(offy+1),dstp)[0]

        for kkk in range(pcnum0):
            count=1
            for ks in np.linspace(-10,10,11):
                pnn = np.zeros([len(pc[0])])
                for k in range(Nbb):
                    if k == kkk:
                        pnn=np.add(pnn,pc.T[k]*(mss[k]+ks*sss[k])) #pc[k] has sign issue again
                    else:
                        pnn=pnn+pc.T[k]*mss[k]
                pnn = np.multiply(pnn,sdd.T) + mdd.T
                xx = pnn[0:Nbb]
                yy = pnn[Nbb:]
                xx = np.append(xx,xx[0])
                yy = np.append(yy,yy[0])
                plt.figure(1)
                plt.plot(xx+offx[kkk],yy+offy[kkk],'-',color=cid.to_rgba(count))
                count = count + 1
        plt.axis('equal')
    # check III- reconstruct the cell shape using principle
    if True:
        pnn=np.zeros(len(pc[0]))
        for k in range(pcnum0):
            pnn = pnn + pc.T[k] * ce1[k]
        pnn=np.multiply(pnn,sdd.T) + mdd.T
        xx=pnn[0:Nbb]
        yy=pnn[Nbb:]
        xx=np.append(xx,xx[0])
        yy=np.append(yy,yy[0])
        plt.figure(33)
        plt.plot(np.append(xr,xr[0]),np.append(yr,yr[0]),'r-',xx,yy,'b-')
        plt.axis('equal')
        plt.axis('off')
    count=1
    pnn=np.zeros(len(pc[0]))
    for k in range(pcnum0):
        pnn=pnn + np.multiply(pc.T[k],mss[k])
    pnn=np.multiply(pnn,sdd.T) + mdd.T
    xx=pnn[0:Nbb]
    yy=pnn[Nbb:]
    xx=np.append(xx,xx[0])
    yy=np.append(yy,yy[0])
    plt.figure(1311)
    plt.plot(xx,yy,'b-',linewidth=2.0)
    plt.axis('equal')
    plt.axis('off')
    #if ch == 'ch2': plt.show()
    return pc,score,latent,VamModel

def pca_bdreg_main(bdpc,VamModel,BuildModel,ch):
    start = time.time()
    pc,score,latent,VamModel=pca_bdreg_v1(bdpc,VamModel,BuildModel,ch)
    end = time.time()
    print ('For PCA, elapsed time is ' + str(end-start) + 'seconds...')
    return pc, score, latent, VamModel
