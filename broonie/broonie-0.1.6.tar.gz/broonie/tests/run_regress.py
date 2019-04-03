import time as tm
import pandas as pd
import numpy as np
from broonie.regress import regressDataClass

print('Begin regress')

inIndices = 'dfIndices.tsv'
inDistances = 'dfDistances.tsv'
inRdata = '/projects/sequence_analysis/vol1/prediction_work/CausalInference/CausalNetworking_forKirk/PCAProjectionImputationPipeline/MouseTumor_allMice_allGenes_Rawdata/mouse_raw_data_allcells_Notscaled.tsv'

knn=10
###################################################### group effect
# Straight up regression using the indices/distance and Raw data set. Default covariates are selected
print('Run regressions')

inputrawfilename = inRdata
yindexfilename = inIndices
ydistancefilename = inDistances
outputRfilename ='newRoutput-testing.tsv'
outputSfilename ='newSoutput-testing.tsv'
z = regressDataClass(knn,inputrawfilename,yindexfilename,ydistancefilename,outputRfilename,outputSfilename)
z.reportParameters()
z.runProcess()
z.writeNewR()
z.writeNewS()

###################################################### group effect
# Use the filebased techniques for specifying possible effect names
# batchfile must contain ALL possible effects in the data set
batchfilename='listOfBatchEffects.txt'
inputrawfilename = inRdata
yindexfilename = inIndices
ydistancefilename = inDistances
outputRfilename ='newRoutput-testing2.tsv'
outputSfilename ='newSoutput-testing2.tsv'
z = regressDataClass(knn,inputrawfilename,yindexfilename,ydistancefilename,outputRfilename,outputSfilename,batchfilename)
z.reportParameters()
z.runProcess()
z.writeNewR()
z.writeNewS()



