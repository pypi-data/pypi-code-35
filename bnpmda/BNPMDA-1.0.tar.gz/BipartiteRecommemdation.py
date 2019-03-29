#!/usr/bin/python
# -*- coding: UTF-8 -*-
# encoding: GBK

import operator
from math import e

import numpy as np
import scipy.cluster.hierarchy as sch
import xlrd

M = 495; N = 383;K_CONECT = 5430
Y = np.zeros((M ,N))   #生成495行 383列的零矩阵Y
S_r = np.zeros((M ,M))  #生成495行 383列的零矩阵S_r
S_d = np.zeros((N ,N))   #生成495行 383列的零矩阵S_d

f_DSEMANTIC_1 = open(r'.\Data\disease semantic similarity1.txt') #疾病相似矩阵1
f_DSEMANTIC_2 = open(r'.\Data\disease semantic similarity2.txt') #疾病相似矩阵2
f_RFUNCTIONAL = open(r'.\Data\miRNA functional similarity.txt')#miRNA功能相似性矩阵
f_DN = xlrd.open_workbook(r'.\Data\diseasenumber.xlsx')#
f_RN = xlrd.open_workbook(r'.\Data\miRNAnumber.xlsx')
fw_PredictResult= open(".\predictedresult.txt","w")


F1=[]
lines_1=f_DSEMANTIC_1.readlines()
for i in range(N):
    line_1=[float(x) for x in lines_1[i].split()]
    F1.append(line_1)
dSemanticArray_1 = np.array(F1)                #转成数组

F2=[]
lines_2=f_DSEMANTIC_2.readlines()
for j in range(N):
    line_2=[float(x) for x in lines_2[j].split()]
    F2.append(line_2)
dSemanticArray_2 = np.array(F2)                #转成数组

F3=[]
lines_3=f_RFUNCTIONAL.readlines()
for j in range(M):
    line_3=[float(x) for x in lines_3[j].split()]
    F3.append(line_3)
rFunctionalArray = np.array(F3)               #转成数组

dSemanticArray = (dSemanticArray_1+dSemanticArray_2)/2    #两数组相加除以2


f_DWeight = open(r'.\Data\disease semantic similarity weight.txt')
FDW=[]
linesDW=f_DWeight.readlines()
for i in range(N):
    lineDW=[float(x) for x in linesDW[i].split()]
    FDW.append(lineDW)
dWeightArray = np.array(FDW)                #转成数组

f_RWeight = open(r'.\Data\miRNA functional similarity weight.txt')
FRW=[]
linesRW=f_RWeight.readlines()
for i in range(M):
    lineRW=[float(x) for x in linesRW[i].split()]
    FRW.append(lineRW)
rWeightArray = np.array(FRW)               #转成数组

f_MDI = xlrd.open_workbook('.\Data\miRNA-disease.xlsx')
KnownAssociation = []
for i in range(K_CONECT):               #K_CONECT = 5430
    rnarow = int(f_MDI.sheet_by_name('miRNA-disease').cell_value(i,0))-1
    disrow = int(f_MDI.sheet_by_name('miRNA-disease').cell_value(i,1))-1
    Y[rnarow][disrow] = 1
    KnownAssociation.append([disrow,rnarow])
Gama_d1 = 1.

GuassD=np.zeros((N,N))
Gama_d=N*Gama_d1/sum(sum(Y * Y)) 
for i in range(N):
    for j in range(N):
        GuassD[i][j]=e**(-Gama_d*(np.dot(Y[:,i]-Y[:,j],Y[:,i]-Y[:,j])))
Gama_m1 = 1.

GuassR=np.zeros((M,M))
Gama_m=M*Gama_m1/sum(sum(Y * Y)) 
for i in range(M):
    for j in range(M):
        GuassR[i][j]=e**(-Gama_m*(np.dot(Y[i,:]-Y[j,:],Y[i,:]-Y[j,:])))

for i in range(N):
    for j in range(N):
        if dWeightArray[i][j] == 1:
            S_d[i][j] = dSemanticArray[i][j]
        elif dWeightArray[i][j] == 0:
            S_d[i][j] = GuassD[i][j]

for i in range(M):
    for j in range(M):
        if rWeightArray[i][j] == 1:
            S_r[i][j] = rFunctionalArray[i][j]
        elif rWeightArray[i][j] == 0:
            S_r[i][j] = GuassR[i][j]

KnownAssociation.sort()
diseaseKnownNum = [];
TotalDisRelatedRNA = []
for i in range(len(KnownAssociation)):
    if i == 0:
        diseaseKnownNum.append(KnownAssociation[i][0])  
        OneDisRelatedRNA = []
        OneDisRelatedRNA.append(KnownAssociation[i][1])
    elif KnownAssociation[i][0] != KnownAssociation[i - 1][0]:
        diseaseKnownNum.append(KnownAssociation[i][0])
        
        TotalDisRelatedRNA.append(OneDisRelatedRNA)  
        OneDisRelatedRNA = [] 
        OneDisRelatedRNA.append(KnownAssociation[i][1])
    else:
        OneDisRelatedRNA.append(KnownAssociation[i][1])
TotalDisRelatedRNA.append(OneDisRelatedRNA)  
k = 0;
r = np.zeros((N, M))
for everydisease in diseaseKnownNum:

    if len(TotalDisRelatedRNA[k]) > 1:
        ssR = np.zeros((len(TotalDisRelatedRNA[k]), len(TotalDisRelatedRNA[k])))
        for i in range(len(TotalDisRelatedRNA[k])):
            for j in range(len(TotalDisRelatedRNA[k])):
                ssR[i][j] = S_r[TotalDisRelatedRNA[k][i]][TotalDisRelatedRNA[k][j]]
        
        OnesR = np.ones((len(ssR[0]), len(ssR[0])))
        disMat = OnesR - ssR
       
        Z = sch.linkage(disMat, method='ward')
     
        cluster = sch.fcluster(Z, t=1.1)
        maxClusterR = 0;
        for i in range(len(cluster)):
            if cluster[i] > maxClusterR:
                maxClusterR = cluster[i]
        everydisSetNUm = [];
        totalNum = 0
        for bigNum in range(1, maxClusterR + 1):
            thisNum = 0
            for i in range(len(cluster)):
                if cluster[i] == bigNum: 
                    thisNum += 1
                    totalNum += 1
            everydisSetNUm.append(thisNum) 
        for j in range(len(TotalDisRelatedRNA[k])):
            r[everydisease][TotalDisRelatedRNA[k][j]] = float(everydisSetNUm[cluster[j] - 1]) / totalNum
    else:
        r[everydisease][TotalDisRelatedRNA[k][0]] = 1
    k += 1

r_cap = np.zeros((N, M));
Rfin = np.zeros((N, M));
r_bar = []
for i in range(N):
    sumYid = sum(Y[:, i])
    if sumYid == 0:
        r_bar.append(0);
        continue
    rbar = float(sum(r[i, :])) / float(sumYid)
    r_bar.append(rbar)
    tr = max(r[i])
    for j in range(M):
        if r[i][j] < rbar and r[i][j] != 0:
            r_cap[i][j] = (tr - r[i][j]) / rbar
        elif r[i][j] != 0:
            r_cap[i][j] = r[i][j] / rbar
rcsum = []
for j in range(M):
    rcsum.append(sum(r_cap[:, j]))
rsum = []
for i in range(N):
    rsum.append(sum(r[i, :]))
kdiscouter = 0
for thisdisease in range(N):
    if sum(Y[:, thisdisease]) != 0:
        R = [];
        R_inter = np.zeros((N, M));
        Rfin_inter = np.zeros((N, M));
        for i in range(N):
            for j in TotalDisRelatedRNA[kdiscouter]:
                if rcsum[j] != 0:
                    R_inter[i][j] = r_cap[i][j] * r_cap[thisdisease][j] / float(rcsum[j])
            R.append(sum(R_inter[i, :]))
        kcounter = 0
        for i in range(N):
            rsumtemp = rsum[i]
            if rsumtemp != 0:
                Rtemp = R[i]
                for j in TotalDisRelatedRNA[kcounter]:
                    Rfin_inter[i, j] = r[i][j] * Rtemp / float(rsumtemp)
                kcounter += 1
        for j in range(M):
            Rfin[thisdisease][j] = sum(Rfin_inter[:, j])
        kdiscouter += 1

RfinT = Rfin.T

KnownAssociation.sort(key=operator.itemgetter(1))  
RNAKnownNum = [];
TotalRNARelatedDis = []
for i in range(len(KnownAssociation)):
    if i == 0:
        RNAKnownNum.append(KnownAssociation[i][1])  
        OneDisRelatedRNA = []
        OneDisRelatedRNA.append(KnownAssociation[i][0])
    elif KnownAssociation[i][1] != KnownAssociation[i - 1][1]:
        RNAKnownNum.append(KnownAssociation[i][1])
       
        TotalRNARelatedDis.append(OneDisRelatedRNA) 
        OneDisRelatedRNA = []  
        OneDisRelatedRNA.append(KnownAssociation[i][0])
    else:
        OneDisRelatedRNA.append(KnownAssociation[i][0])
TotalRNARelatedDis.append(OneDisRelatedRNA)  
k = 0;
r = np.zeros((M, N))
for everyRNA in RNAKnownNum:
   
    if len(TotalRNARelatedDis[k]) > 1:
        ssD = np.zeros((len(TotalRNARelatedDis[k]), len(TotalRNARelatedDis[k])))
        for i in range(len(TotalRNARelatedDis[k])):
            for j in range(len(TotalRNARelatedDis[k])):
                ssD[i][j] = S_d[TotalRNARelatedDis[k][i]][TotalRNARelatedDis[k][j]]
       
        OnesD = np.ones((len(ssD[0]), len(ssD[0])))
        disMatD = OnesD - ssD
        
        ZDD = sch.linkage(disMatD, method='ward')
       
        clusterD = sch.fcluster(ZDD, t=1.1)
        maxClusterD = 0;
        for i in range(len(clusterD)):
            if clusterD[i] > maxClusterD:
                maxClusterD = clusterD[i]
        everyrnaSetNUm = [];
        totalNum = 0
        for bigNum in range(1, maxClusterD + 1):
            thisNum = 0
            for i in range(len(clusterD)):
                if clusterD[i] == bigNum: 
                    thisNum += 1
                    totalNum += 1
            everyrnaSetNUm.append(thisNum)  
        for j in range(len(TotalRNARelatedDis[k])):
            r[everyRNA][TotalRNARelatedDis[k][j]] = float(everyrnaSetNUm[clusterD[j] - 1]) / totalNum
    else:
        r[everyRNA][TotalRNARelatedDis[k][0]] = 1
    k += 1

r_cap = np.zeros((M, N));
Rfin = np.zeros((M, N));
r_bar = []
for i in range(M):
    sumYir = sum(Y[i, :])
    if sumYir == 0:
        r_bar.append(0)
        continue
    rbar = float(sum(r[i, :])) / float(sumYir)
    r_bar.append(rbar)
    tr = max(r[i])
    for j in range(N):
        if r[i][j] < rbar and r[i][j] != 0:
            r_cap[i][j] = (tr - r[i][j]) / rbar
        elif r[i][j] != 0:
            r_cap[i][j] = r[i][j] / rbar
rcsum = []
for j in range(N):
    rcsum.append(sum(r_cap[:, j]))
rsum = []
for i in range(M):
    rsum.append(sum(r[i, :]))
krnacounter = 0;
for thisRNA in range(M):
    if sum(Y[thisRNA, :]) != 0:
        R = [];
        R_inter = np.zeros((M, N));
        Rfin_inter = np.zeros((M, N));
        for i in range(M):
            for j in TotalRNARelatedDis[krnacounter]:
                if rcsum[j] != 0:
                    R_inter[i][j] = r_cap[i][j] * r_cap[thisRNA][j] / float(rcsum[j])
            R.append(sum(R_inter[i, :]))
        kcounter = 0;
        for i in range(M):
            rsumtemp = rsum[i]
            if rsumtemp != 0:
                Rtemp = R[i]
                for j in TotalRNARelatedDis[kcounter]:
                    Rfin_inter[i, j] = r[i][j] * Rtemp / float(rsumtemp)
                kcounter += 1
        for j in range(N):
            Rfin[thisRNA][j] = sum(Rfin_inter[:, j])
        krnacounter += 1

RDfin = (Rfin + RfinT) * 0.5

Exc = []
for i in range(M):
    for j in range(N):
        if Y[i][j] != 1:
            ListNew = [RDfin[i][j],j,i]
            Exc.append(ListNew)
Exc.sort(reverse=True)
sheet2 = f_DN.sheet_by_name('Sheet1')
sheet3 = f_RN.sheet_by_name('Sheet1')
for i in range(len(Exc)):
    fw_PredictResult.writelines([str(sheet2.cell(Exc[i][1],1).value),"\t",str(sheet3.cell(Exc[i][2],1).value),"\t",str(Exc[i][0]),"\n"])
fw_PredictResult.close()


