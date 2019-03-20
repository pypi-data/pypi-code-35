#!/usr/bin/env python

# internal libraries
from __future__ import division
from copy import deepcopy
from inspect import getargspec
import time
import os
# external libraries
import pandas as pd
import numpy as np
from scipy import stats, cluster, spatial
from sklearn.cluster import KMeans
from sklearn import preprocessing
import matplotlib as mpl
mpl.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter
# my files
from PCA import *

def clusterSM(folder,modelname,score,pc,bdpc,clnum=None,pcnum=None,VamModel=None,BuildModel=None,ch=None):
    print('# clusterSM')
    np.set_printoptions(precision=4,suppress=True)
    #desktop = os.path.join(os.environ["HOMEPATH"],"Desktop")
    folder = os.path.abspath(folder)
    desktop = os.path.join(folder,modelname)
    if BuildModel : desktop = os.path.join(desktop,ch+'_buildmodel')
    else : desktop = os.path.join(desktop,ch+'_applymodel')
    print desktop
    if not os.path.exists(desktop):
        os.makedirs(desktop)
    Nuu=int(round(len(bdpc.T[0])))
    Nbb=int(round(len(bdpc[0]) / 2))
    mmx=np.dot(np.ones([Nuu,1]),np.mean([bdpc],axis=1))
    smx=np.ones(bdpc.shape)
    mdd=mmx[0]
    sdd=smx[0]
    mss=np.mean(score,axis=0)
    sss=np.std(score,axis=0)

    NN=10

    if clnum==None:
        clnum=15
    if pcnum==None:
        pcnum=20

    if BuildModel:
        VamModel['clnum']=clnum
        VamModel['pcnum']=pcnum
    else:
        clnum = VamModel['clnum']
        pcnum = VamModel['pcnum']
        pc = VamModel['pc']

    cms00 = score[:,0:pcnum]
    cms = deepcopy(cms00)

    if BuildModel:
        mincms=np.amin(cms,axis=0)
        VamModel['mincms']=mincms
        VamModel['boxcoxlambda']=np.zeros(len(cms.T))
        VamModel['testmean']=np.zeros(len(cms.T))
        VamModel['teststd']=np.zeros(len(cms.T))
    else:
        mincms=VamModel['mincms']

    for k in range(len(cms.T)):
        test=cms.T[k]
        test=test - mincms[k] + 1
        if BuildModel:
            test,maxlog=stats.boxcox(test)
            test = np.asarray(test)
            #####################
            VamModel['boxcoxlambda'][k]=maxlog
            VamModel['testmean'][k]=np.mean(test)
            VamModel['teststd'][k]=np.std(test)
            #####################
            cms.T[k]=(test-np.mean(test))/np.std(test)
        else:
            test=stats.boxcox(test,VamModel['boxcoxlambda'][k])
            cms.T[k]=(test-VamModel['testmean'][k])/VamModel['teststd'][k]

    cms0=deepcopy(cms)
    cmsn=deepcopy(cms)

    if BuildModel:
        cmsn_Norm = preprocessing.normalize(cmsn)
        if isinstance(clnum, basestring):
            clnum = int(clnum)

        kmeans=KMeans(n_clusters=clnum,init='k-means++',n_init=3,max_iter=300).fit(cmsn_Norm) #init is plus,but orginally cluster, not available in sklearn
        IDX = kmeans.labels_
        C = kmeans.cluster_centers_
        ##################
        VamModel['C']=C
        D = spatial.distance.cdist(cmsn,VamModel['C'])
        IDX = np.argmin(D,axis=1)
    else:
        C = VamModel['C']
        D = spatial.distance.cdist(cmsn,VamModel['C'])
        IDX = np.argmin(D,axis=1)
        ##################
    clnum=max(IDX)+1
    offx,offy=np.meshgrid(range(clnum),[0])
    offx=np.multiply(offx,1)+1
    offx=offx[0]*1-0.5
    offy=np.subtract(np.multiply(offy,1), 1.5)+1
    offy=offy[0]
    cmap = plt.cm.jet
    vmax = int(clnum*10)
    norm = mpl.colors.Normalize(vmin=0,vmax=vmax)
    cid = plt.cm.ScalarMappable(norm=norm,cmap=cmap)

    clshape=np.zeros([clnum,len(cms00[0])])
    clshapesdv=deepcopy(clshape)
    bdst0=np.empty(len(bdpc.T))
    bdst=deepcopy(bdst0)
    for kss in range(clnum):
        c88=IDX == kss
        bdpcs=bdpc[c88,:]
        mbd=np.mean(bdpcs,axis=0)
        bdst0=np.vstack((bdst0,mbd))
    bdst0=bdst0[1:]
    # dendrogram of the difference between different shape
    if BuildModel:
        Y=spatial.distance.pdist(bdst0,'euclidean')
        Z=cluster.hierarchy.linkage(Y,method='complete') #4th row is not in matlab
        Z[:,2] = Z[:,2]*10 #multiply distance manually 10times to plot better.
        cluster.hierarchy.set_link_color_palette(['k'])
        fig = plt.figure(289,figsize=(6,3),linewidth=2.0,frameon=False)
        plt.yticks([])
        R=cluster.hierarchy.dendrogram(Z,p=0,truncate_mode='mlab',orientation='bottom',ax=None,above_threshold_color='k')
        leaflabel = np.array(R['ivl'])
        dendidx = leaflabel
        VamModel['dendidx']=dendidx
        cluster.hierarchy.set_link_color_palette(None)
        fig.savefig(os.path.join(desktop,"representative shape number dendrogram_"+ch+".png"))
    else:
        dendidx = VamModel['dendidx']
    plt.axis('equal')
    plt.axis('off')
    IDXsort=np.zeros(len(IDX))
    for kss in range(clnum):
        c88=IDX == int(dendidx[kss])
        IDXsort[c88]=kss
    IDX=deepcopy(IDXsort)
    bdsubtype=np.empty((int(max(IDX)+1),2,Nbb+1)) #need more specific preallocation: 2 for x and y, Nbb+1 for len(x)
    for kss in range(int(max(IDX))+1):
        c88=IDXsort == kss
        clshape[kss]=np.mean(cms00[c88],axis=0)
        clshapesdv[kss]=np.std(cms00[c88],axis=0)
        pnn=np.zeros(len(pc.T[0]))
        for kev in range(len(cms00[0])):
            pnn=np.add(pnn,np.multiply(pc.T[kev],clshape[kss,kev]))
            pnnlb=np.add(pnn,np.multiply(np.multiply(pc.T[kev],-2),clshapesdv[kss,kev]))
            pnnhb=np.add(pnn,np.multiply(np.multiply(pc.T[kev],2),clshapesdv[kss,kev]))
        pnn=np.multiply(pnn,sdd) + mdd
        pnnlb=np.multiply(pnnlb,sdd) + mdd
        pnnhb=np.multiply(pnnhb,sdd) + mdd  #pnn,pnnlb&hb are all randomized
        xx=pnn[0:Nbb]
        yy=pnn[Nbb:]
        xlb=pnnlb[0:Nbb]
        ylb=pnnlb[Nbb:]
        xhb=pnnhb[0:Nbb]
        yhb=pnnhb[Nbb:]
        xx=np.append(xx,xx[0])
        yy=np.append(yy,yy[0])
        xxhb=np.append(xhb,xhb[0])
        yyhb=np.append(yhb,yhb[0])
        xxlb=np.append(xlb,xlb[0])
        yylb=np.append(ylb,ylb[0])
        fss=4
        plt.figure(289,figsize=(6,3))
        plt.axis('equal')
        plt.plot((xx/fss+offx.T[kss])*10, (yy/fss+offy.T[kss])*10, '-',color=cid.to_rgba(kss)) #this is not plotted in matlab as well
        bdsubtype[kss][0]=xx/fss
        bdsubtype[kss][1]=yy/fss
        bdpcs=bdpc[c88]
        mbd=np.mean(bdpcs,axis=0)
        bdNUM=int(round(len(mbd)/2))
        bdst=np.vstack((bdst,mbd))
        xaxis = np.add(np.divide(np.append(mbd[0:bdNUM],mbd[0]),fss),offx[kss])*10
        yaxis = np.add(np.divide(np.append(mbd[bdNUM:],mbd[bdNUM]),fss),offy[kss])*10
        figeach= plt.figure(7)
        plt.plot(xaxis,yaxis,'-')
        plt.gca().invert_yaxis()
        plt.axis('off')
        figeach.savefig(os.path.join(desktop,"representative shape "+dendidx[kss]+".png"))
        plt.clf()
        plt.figure(289,figsize=(6,3))
        plt.plot(xaxis,yaxis,'-') #this is the shape of the dendrogram
        sid=np.argsort(np.random.rand(sum(c88),1),axis=0)
        if len(sid)<NN: enum = len(sid)
        else:enum = NN
        for knn in range(enum):
            plt.figure(922)
            x99=bdpcs[sid[knn],np.append(range(bdNUM),0)]
            y99=bdpcs[sid[knn],np.append(np.arange(bdNUM,(bdNUM*2),1),bdNUM)]
            xax = np.add(np.divide(x99,fss),offx[kss])
            yax = np.add(np.divide(y99,fss),offy[kss])
            plt.plot(xax,yax,'r-',linewidth=0.1)
    bdst = bdst[1:]
    # result visulation
    fig922=plt.figure(922)
    plt.axis('equal')
    plt.axis('off')
    fig922.savefig(os.path.join(desktop,"representative shapes_"+ch+".png"))
    fig289=plt.figure(289,figsize=(6,3))
    plt.axis('equal')
    plt.axis('off')
    fig289.savefig(os.path.join(desktop,"representative shape dendrogram_"+ch+".png"))
    crap=np.sort(IDX)
    sid=np.argsort(IDX)
    BMsort=cmsn[sid]
    fig20=plt.figure(20)
    plt.imshow(cmsn,extent=[0,1,0,1])
    plt.clim(-1,1)
    plt.gca().xaxis.set_minor_formatter(NullFormatter())
    plt.yticks()
    plt.gca().yaxis.set_minor_formatter(NullFormatter())
    fig21=plt.figure(21)
    plt.imshow(BMsort,extent=[0,1,0,1])
    plt.gca().tick_params(direction='out')
    plt.yticks()
    plt.gca().yaxis.set_minor_formatter(NullFormatter())
    fig23=plt.figure(23)
    crap = np.expand_dims(crap,axis=1)
    imgplot = plt.imshow(crap,cmap='jet',extent=[0,1,0,1]) #imagesc(crap)
    plt.axis('on')
    plt.xticks()
    plt.gca().xaxis.set_minor_formatter(NullFormatter())
    plt.yticks()
    plt.gca().yaxis.set_minor_formatter(NullFormatter())
    plt.close()
    n,bins,patches = plt.hist(IDX,range(clnum+1))
    plt.close()
    fig22 = plt.figure(22)
    n=np.divide(n,np.sum(n))
    n=np.multiply(n,100)
    n=np.around(n,2)
    plt.bar(x=np.delete(bins,0)-1,height=n,width=0.5,align='center',color='blue',edgecolor='black')
    plt.xticks(np.delete(bins,0)-1)
    plt.ylabel('%')
    fig22.savefig(os.path.join(desktop,'representative shape distribution_'+ch+'.png'))
    plt.close('all')
    return IDX,bdsubtype,C,VamModel

def cluster_main(folder,modelname,score,pc,bdpc,clnum=None,pcnum=None,VamModel=None,BuildModel=None,cellornuc=None):
    print('## clusterSM.py')
    start = time.time()
    IDX,bdsubtype,C,VamModel=clusterSM(folder,modelname,score,pc,bdpc,clnum,pcnum,VamModel,BuildModel,cellornuc)
    end = time.time()
    print('For cluster, elapsed time is ' + str(end-start) + 'seconds...')
    return IDX,bdsubtype,C,VamModel