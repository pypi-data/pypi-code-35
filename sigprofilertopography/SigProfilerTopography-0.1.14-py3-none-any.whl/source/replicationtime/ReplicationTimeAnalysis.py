# This source code file is a part of SigProfilerTopography
# SigProfilerTopography is a tool included as part of the SigProfiler
# computational framework for comprehensive analysis of mutational
# signatures from next-generation sequencing of cancer genomes.
# SigProfilerTopography provides the downstream data analysis of
# mutations and extracted mutational signatures w.r.t.
# nucleosome occupancy, replication time, strand bias and processivity.
# Copyright (C) 2018 Burcak Otlu



#############################################################
# This python code generates normalized mutation density data for different analyses types which are
# Using all mutations (all chromosomes, all samples, signatures) which leads to Aggregated Substitutions
# Using all mutations but in signature based manner leads to Signature Based
# Using all mutations in signature based and sample based manner leads to Signature based and Sample Based
# Using all indels (all chromosomes, all samples) which leads to Aggregated Indels
# Using all indels (diving indels of length >=3 as microhomology-mediated indels and indels of length <3 as repeat-mediated  indels)

## In this python code
## I read the wavelet-transformed signal wig across whole genome
## Sort the signal in descending order
## Divide the data into 10 equal deciles
## Return 10 deciles as data frames
## Read the mutation file
## Group by mutation file by chromosome
## Group by decile file by chromosome
## For each chromosome (Done in the loop sequentially)
## Make a list of input
## chromosome based mutation file mutation file
## chromosome based decile files coming from 10 different deciles (Done in parallel for all of the 10 deciles)
## In the function I will generate interval tree from decile file
## Overlap the mutations with the interval tree
## Return the total number of mutations that overlap between mutation file and decile file
## Get chromosome based mutation file
## Get chromosome based decile file
## Accumulate the total number of mutations that overlap for each decile file
#############################################################

#############################################################
# Constraints, Thresholds
# Please note that for sample based and signature based replication time analysis
# We consider samples with at least 3000 mutations at total in all deciles.
#############################################################

import os
import sys
import twobitreader

#############################################################
current_abs_path = os.path.abspath(os.path.dirname(__file__))
print('ReplicationTimeAnalysis.py current_abs_path:%s' %(current_abs_path))
#############################################################


commonsPath = os.path.join(current_abs_path, '..','commons')
sys.path.append(commonsPath)

from SigProfilerTopography.source.commons.TopographyCommons import *


#Global variables
THRESHOLD_NUMBER_OF_MUTATIONS = 3000


##################################################################
def process(wavelet_unprocessed_df):
    #Read the file and generate chr start end signal wavelet_smoothed_signal
    #Then sort the data w.r.t. signal in descending order
    #Divide the data into 10 equal deciles
    #Return 10 deciles: the first decile is the earliest one and the tenth decile is the latest one

    columns = ['chr', 'start', 'end','signal']

    #Create an empty dataframe
    wavelet_processed_df = pd.DataFrame(columns=columns)

    # print('############### empty wavelet_processed_df starts #################')
    # print(wavelet_processed_df.shape)
    # print(wavelet_processed_df.head())
    # print('############### empty wavelet_processed_df ends #################')

    #dummy initialization
    i = 0
    chrom = 'chr1'
    start = 0
    step = 1000

    rows_list = []

    # e.g. rows
    # fixedStep chrom=chr1 start=24500 step=1000 span=1000
    # 57.4679
    # 57.467
    # 57.4651
    # 57.4623
    # 57.4586
    # 57.454
    # 57.4484
    # 57.442
    # 57.4347
    # 57.4266
    # 57.4176


    for row in wavelet_unprocessed_df.itertuples(index=True, name='Pandas'):
        # row's type is <class 'pandas.core.frame.Pandas'>
        # row[0] is the index
        # row[1] is fixedStep chrom=chr1 start=24500 step=1000 span=1000 or 57.4679
        if (row[1].startswith('fixedStep')):
            #This is the information line
            chrom = row[1].split()[1].split('=')[1]
            start = int(row[1].split()[2].split('=')[1])
            step = int(row[1].split()[3].split('=')[1])
        else:
            signal = float(row[1])
            chr = chrom
            start = start
            end = start + step-1
            dict = {'chr':chr, 'start':start, 'end':end, 'signal':signal}
            rows_list.append(dict)
            start += step

    # print('Number of intervals to be inserted in wavelet_processed_df: %d' %len(rows_list))

    #rows_list contain the list of row where each row is a dictionary
    wavelet_processed_df = pd.DataFrame(rows_list, columns=['chr','start','end','signal'])

    # print('debug starts')
    # print('############### wavelet_processed_df is filled starts #################')
    # print(wavelet_processed_df.shape)
    # print(wavelet_processed_df.head())
    # print('############### wavelet_processed_df is filled ends #################')
    # print('debug ends')

    return wavelet_processed_df
##################################################################




##################################################################
def readRepliSeqTimeData(pool,repliseqDataFilename,genome):
    ###################################################################
    ############### Read MCF-7 RepliSeq Time data starts ##############
    ###################################################################
    #Read the wavelet signal
    wavelet_unprocessed_df = readWaveletSmoothedRepliSeqSignal(repliseqDataFilename)

    #Process the wavelet signal, convert into interval version
    # here column names are added columns = ['chr', 'start', 'end','signal']
    wavelet_processed_df = process(wavelet_unprocessed_df)
    # print('wavelet_processed_df.shape processed interval version')
    # print(wavelet_processed_df.shape)

    chrNamesInReplicationTimeDataArray = wavelet_processed_df['chr'].unique()


    #Augment wavelet_processed_df with numberofAttributableBases
    wavelet_processed_augmented_df = augment(pool,wavelet_processed_df,genome)

    #Sort the wavelet processed df in descending order w.r.t. signal column
    # print('############ before sort wavelet_processed_augmented_df ###################')
    # print(wavelet_processed_augmented_df.head())
    # print('############ before sort wavelet_processed_augmented_df ###################')

    #Sort in descending order
    #Higher the replication time signal earlier the replication is
    wavelet_processed_augmented_df.sort_values('signal', ascending=False, inplace=True)

    # print('############ after sort wavelet_processed_augmented_df ###################')
    # print(wavelet_processed_augmented_df.head())
    # print('############ after sort wavelet_processed_augmented_df ###################')

    #Split wavelet_processed_augmented_df into 10 deciles
    deciles = np.array_split(wavelet_processed_augmented_df,10)
    # print('Number of decile:%d' %len(deciles))
    #deciles is a list and each decile is a dataframe <class 'pandas.core.frame.DataFrame'>
    #The first decile is the earliest one
    #The last decile is the latest one
    # print('type(deciles):%s' %type(deciles))
    totalNumberofIntervals = 0
    for decile in deciles:
        # print('######################')
        # print('type(decile)"%s' %type(decile))
        # print('Number of elements in each decile: %d' %len(decile))
        totalNumberofIntervals += len(decile)
        # print(decile.head())
        #print(decile.iloc[0])
        #print(decile.iloc[len(decile) - 300000])
        #print(decile.iloc[len(decile) - 200000])
        #print(decile.iloc[len(decile) - 100000])
        #print(decile.iloc[len(decile)-1])
        # print('######################')

    print('totalNumberofIntervals in all deciles : %d' %totalNumberofIntervals)
    return chrNamesInReplicationTimeDataArray, deciles
    ###################################################################
    ############### Read MCF-7 RepliSeq Time data ends ################
    ###################################################################

##################################################################



##################################################################
def getNumberofAttributableBases(wavelet_row, genome):
    start =wavelet_row[1]
    end = wavelet_row[2]
    #In my code ends are inclusive
    #twobitreader uses ends exlusive
    seq = genome.get_slice(start, end+1)
    numofAttributableBases = seq.count('A') + seq.count('T') + seq.count('G') + seq.count('C') + seq.count('a') + seq.count('t') + seq.count('g') + seq.count('c')
    # print('######### debug starts ##############')
    # print(wavelet_row)
    # print('len(seq):%d' %len(seq))
    # print('numofAttributableBases:%d' %numofAttributableBases)
    # print('##########  debug ends #############')
    return numofAttributableBases
##################################################################

##################################################################
def addNumofAttributableBasesColumn(inputList):
    chrLong = inputList[0]
    chrBased_wavelet_processed_df_group =inputList[1]
    genome = inputList[2]
    resulting_df = chrBased_wavelet_processed_df_group.apply(getNumberofAttributableBases, genome = genome[chrLong], axis= 1)

    # print('######## debug numberofAttributableBases starts ########')
    # print('for %s starts' %chrLong)
    # print('len(chrBased_wavelet_processed_df_group): %d ' %len(chrBased_wavelet_processed_df_group))
    # print('len(resulting_df): %d' %len(resulting_df))
    # print('type(chrBased_wavelet_processed_df_group): %s' % type(chrBased_wavelet_processed_df_group))
    # print('type(resulting_df): %s' %type(resulting_df))

    if (len(chrBased_wavelet_processed_df_group)!=len(resulting_df)):
        print('There is a situation: len(chrBased_wavelet_processed_df_group) is not equal  to len(resulting_df)')

    # print('debug starts')
    # print(resulting_df)
    # print(chrBased_wavelet_processed_df_group.columns.values.tolist())
    # print('debug ends')

    #Add the resulting_df as a new column to chrBased_wavelet_processed_df_group
    chrBased_wavelet_processed_df_group['numofBases'] = resulting_df

    # print('debug starts')
    # print(chrBased_wavelet_processed_df_group.columns.values.tolist())
    # print('debug ends')

    # print('for %s ends' % chrLong)
    # print('######## debug numberofAttributableBases ends ########')

    return (chrLong,chrBased_wavelet_processed_df_group)
##################################################################


##################################################################
#Works for AGGREGATEDSUBSTITUTIONS and SIGNATURES
def searchSub(
        mutation_row,
        subsSignature2NumberofMutationsDict,
        sample2SubsSignature2NumberofMutationsDict,
        chrBasedReplicationTimeDataArrayWithDecileIndex,
        type2DecileIndex2NumberofMutationsDict,
        sample2Type2DecileIndex2NumberofMutationsDict):

    # For single point mutations start and end are the same, therefore we need to add 1 to mutation_row['End']
    start= mutation_row[START]
    end= mutation_row[END]+1

    slicedArray = chrBasedReplicationTimeDataArrayWithDecileIndex[start:end]

    #get the samplename
    sample = mutation_row[SAMPLE]

    # np.nonzero returns the indices of the elements that are non-zero.
    # np.unique finds the unique elements of an array returns ndarray the sorted unique values.
    # np.nditer efficient multi-dimensional iterator object to iterate over arrays.
    uniqueIndexesArray = np.unique(slicedArray[np.nonzero(slicedArray)])

    if (uniqueIndexesArray.size>0):
        for decileIndex in np.nditer(uniqueIndexesArray):
            # type(decileIndex) is numpy.ndarray
            decileIndexNum = int(decileIndex)

            ################### AGGREGATEDSUBSTITUTIONS starts #####################
            decileIndex2NumberofMutationsDict = type2DecileIndex2NumberofMutationsDict[AGGREGATEDSUBSTITUTIONS]
            if decileIndexNum in decileIndex2NumberofMutationsDict.keys():
                decileIndex2NumberofMutationsDict[decileIndexNum] +=1
            else:
                decileIndex2NumberofMutationsDict[decileIndexNum] = 1
            ################### AGGREGATEDSUBSTITUTIONS ends #######################

            ########################### Signatures start ###########################
            for signature in subsSignature2NumberofMutationsDict:
                if mutation_row[signature] >= SUBSTITUTION_MUTATION_SIGNATURE_PROBABILITY_THRESHOLD:
                    decileIndex2NumberofMutationsDict = type2DecileIndex2NumberofMutationsDict[signature]
                    if decileIndexNum in decileIndex2NumberofMutationsDict.keys():
                        decileIndex2NumberofMutationsDict[decileIndexNum] += 1
                    else:
                        decileIndex2NumberofMutationsDict[decileIndexNum] = 1
            ########################### Signatures end #############################

            ############################# Sample Based starts ###########################
            if sample in sample2SubsSignature2NumberofMutationsDict:

                ############## Sample Based Aggregated Substitutions starts ############
                for signature in sample2SubsSignature2NumberofMutationsDict[sample]:
                    if mutation_row[signature] >= SUBSTITUTION_MUTATION_SIGNATURE_PROBABILITY_THRESHOLD:
                        if decileIndexNum in sample2Type2DecileIndex2NumberofMutationsDict[sample][signature]:
                            sample2Type2DecileIndex2NumberofMutationsDict[sample][signature][decileIndexNum] += 1
                        else:
                            sample2Type2DecileIndex2NumberofMutationsDict[sample][signature][decileIndexNum] = 1
                ############## Sample Based Signatures ends ############################

                ############## Sample Based Aggregated Substitutions starts ############
                if decileIndexNum in sample2Type2DecileIndex2NumberofMutationsDict[sample][AGGREGATEDSUBSTITUTIONS]:
                    sample2Type2DecileIndex2NumberofMutationsDict[sample][AGGREGATEDSUBSTITUTIONS][decileIndexNum] += 1
                else:
                    sample2Type2DecileIndex2NumberofMutationsDict[sample][AGGREGATEDSUBSTITUTIONS][decileIndexNum] = 1
                ############## Sample Based Aggregated Substitutions ends ##############
            ############################# Sample Based ends ############################


##################################################################



##################################################################
def searchIndel(indel_row,sample2SignaturesWithAtLeast10KEligibleMutations2NumberofMutationsDict,chrBasedReplicationTimeDataArrayWithDecileIndex,type2DecileIndex2NumberofMutationsDict,sample2Type2DecileIndex2NumberofMutationsDict):
    # For indels start and end are can be different from each other.
    start= indel_row[START]
    end= indel_row[START]+1

    slicedArray = chrBasedReplicationTimeDataArrayWithDecileIndex[start:end]

    #get the samplename
    sample = indel_row[SAMPLE]

    # np.nonzero returns the indices of the elements that are non-zero.
    # np.unique finds the unique elements of an array returns ndarray the sorted unique values.
    # np.nditer efficient multi-dimensional iterator object to iterate over arrays.
    uniqueIndexesArray = np.unique(slicedArray[np.nonzero(slicedArray)])

    if (uniqueIndexesArray.size>0):
        for decileIndex in np.nditer(uniqueIndexesArray):
            # type(decileIndex) is numpy.ndarray
            decileIndexNum = int(decileIndex)

            ################### AGGREGATEDINDELS starts #####################
            decileIndex2NumberofMutationsDict = type2DecileIndex2NumberofMutationsDict[AGGREGATEDINDELS]
            if decileIndexNum in decileIndex2NumberofMutationsDict.keys():
                decileIndex2NumberofMutationsDict[decileIndexNum] +=1
            else:
                decileIndex2NumberofMutationsDict[decileIndexNum] = 1
            ################### AGGREGATEDINDELS ends #######################

            ########################### INDELS start ###########################
            if indel_row[LENGTH] >= 3:
                decileIndex2NumberofMutationsDict = type2DecileIndex2NumberofMutationsDict[MICROHOMOLOGY]
                if decileIndexNum in  decileIndex2NumberofMutationsDict:
                    decileIndex2NumberofMutationsDict[decileIndexNum] += 1
                else:
                    decileIndex2NumberofMutationsDict[decileIndexNum] = 1

            else:
                decileIndex2NumberofMutationsDict = type2DecileIndex2NumberofMutationsDict[REPEAT]
                if decileIndexNum in  decileIndex2NumberofMutationsDict:
                    decileIndex2NumberofMutationsDict[decileIndexNum] += 1
                else:
                    decileIndex2NumberofMutationsDict[decileIndexNum] = 1
            ########################### INDELS end #############################

            ################################ Sample based starts #################################
            if sample in sample2SignaturesWithAtLeast10KEligibleMutations2NumberofMutationsDict:

                type2DecileIndex2NumberofMutationsDict = sample2Type2DecileIndex2NumberofMutationsDict[sample]

                ################### AGGREGATEDINDELS starts #####################
                decileIndex2NumberofMutationsDict = type2DecileIndex2NumberofMutationsDict[AGGREGATEDINDELS]
                if decileIndexNum in decileIndex2NumberofMutationsDict.keys():
                    decileIndex2NumberofMutationsDict[decileIndexNum] += 1
                else:
                    decileIndex2NumberofMutationsDict[decileIndexNum] = 1
                ################### AGGREGATEDINDELS ends #######################

                ########################### INDELS start ###########################
                if indel_row[LENGTH] >= 3:
                    decileIndex2NumberofMutationsDict = type2DecileIndex2NumberofMutationsDict[MICROHOMOLOGY]
                    if decileIndexNum in decileIndex2NumberofMutationsDict:
                        decileIndex2NumberofMutationsDict[decileIndexNum] += 1
                    else:
                        decileIndex2NumberofMutationsDict[decileIndexNum] = 1

                else:
                    decileIndex2NumberofMutationsDict = type2DecileIndex2NumberofMutationsDict[REPEAT]
                    if decileIndexNum in decileIndex2NumberofMutationsDict:
                        decileIndex2NumberofMutationsDict[decileIndexNum] += 1
                    else:
                        decileIndex2NumberofMutationsDict[decileIndexNum] = 1
                ########################### INDELS end #############################
            ################################ Sample based ends ###################################

##################################################################



##################################################################
#Case1 SPMs (AggregatedSubstitutions and Signatures)
def searchForSubs(
        subsSignature2NumberofMutationsDict,
        sample2SubsSignature2NumberofMutationsDict,
        chrBased_subs_df_split,chrBasedReplicationTimeDataArrayWithDecileIndex):

    ############################################################
    # We will fill type2DecileIndex2NumberofMutationsDict for AGGREGATEDSUBSTITUTIONS and for each signature and return it
    type2DecileIndex2NumberofMutationsDict= {}

    # Initialize for AGGREGATEDSUBSTITUTIONS and signatures
    type2DecileIndex2NumberofMutationsDict[AGGREGATEDSUBSTITUTIONS] = {}
    for signature in subsSignature2NumberofMutationsDict:
        type2DecileIndex2NumberofMutationsDict[signature] = {}
    ############################################################

    ############################################################
    #Initialize sample2Type2DecileIndex2NumberofMutationsDict
    sample2Type2DecileIndex2NumberofMutationsDict = {}

    for sample in sample2SubsSignature2NumberofMutationsDict:
        sample2Type2DecileIndex2NumberofMutationsDict[sample] = {}

        sample2Type2DecileIndex2NumberofMutationsDict[sample][AGGREGATEDSUBSTITUTIONS] = {}
        for signature in sample2SubsSignature2NumberofMutationsDict[sample]:
            sample2Type2DecileIndex2NumberofMutationsDict[sample][signature] = {}
    ############################################################

    chrBased_subs_df_split.apply(searchSub,
                                 subsSignature2NumberofMutationsDict=subsSignature2NumberofMutationsDict,
                                 sample2SubsSignature2NumberofMutationsDict= sample2SubsSignature2NumberofMutationsDict,
                                 chrBasedReplicationTimeDataArrayWithDecileIndex= chrBasedReplicationTimeDataArrayWithDecileIndex,
                                 type2DecileIndex2NumberofMutationsDict=type2DecileIndex2NumberofMutationsDict,
                                 sample2Type2DecileIndex2NumberofMutationsDict=sample2Type2DecileIndex2NumberofMutationsDict,
                                 axis=1)

    return type2DecileIndex2NumberofMutationsDict, sample2Type2DecileIndex2NumberofMutationsDict
##################################################################


##################################################################
#  Please notice that Case2 uses the search methods for Case1 and Case3
##################################################################






##################################################################
#Case3 Indels (AggregatedIndels and Indel Types)
def searchForIndels(sample2SignaturesWithAtLeast10KEligibleMutations2NumberofMutationsDict,chrBased_indels_df_split,chrBasedReplicationTimeDataArrayWithDecileIndex):

    ############################################################
    # We will fill type2DecileIndex2NumberofMutationsDict for AGGREGATEDSUBSTITUTIONS and for each signature and return it
    type2DecileIndex2NumberofMutationsDict= {}

    # Initialize for AGGREGATEDINDELS and indels tpes
    type2DecileIndex2NumberofMutationsDict[AGGREGATEDINDELS] = {}
    type2DecileIndex2NumberofMutationsDict[MICROHOMOLOGY] = {}
    type2DecileIndex2NumberofMutationsDict[REPEAT] = {}
    ############################################################


    ############################################################
    #TODO initialize sample2Type2DecileIndex2NumberofMutationsDict
    sample2Type2DecileIndex2NumberofMutationsDict = {}
    for sample in sample2SignaturesWithAtLeast10KEligibleMutations2NumberofMutationsDict:
        sample2Type2DecileIndex2NumberofMutationsDict[sample] = {}

        sample2Type2DecileIndex2NumberofMutationsDict[sample][AGGREGATEDINDELS] = {}
        sample2Type2DecileIndex2NumberofMutationsDict[sample][MICROHOMOLOGY] = {}
        sample2Type2DecileIndex2NumberofMutationsDict[sample][REPEAT] = {}
    ############################################################


    chrBased_indels_df_split.apply(searchIndel,
                                   sample2SignaturesWithAtLeast10KEligibleMutations2NumberofMutationsDict=sample2SignaturesWithAtLeast10KEligibleMutations2NumberofMutationsDict,
                                   chrBasedReplicationTimeDataArrayWithDecileIndex= chrBasedReplicationTimeDataArrayWithDecileIndex,
                                   type2DecileIndex2NumberofMutationsDict=type2DecileIndex2NumberofMutationsDict,
                                   sample2Type2DecileIndex2NumberofMutationsDict= sample2Type2DecileIndex2NumberofMutationsDict,
                                   axis=1)
    return type2DecileIndex2NumberofMutationsDict, sample2Type2DecileIndex2NumberofMutationsDict
##################################################################



##################################################################
#Please notice that replication time data are not overlappig data therefore only setting one decileOndex will be correct.
# e.g.:
# start end
#   10 1009
# 1010 2009
def fillArray(chrBased_replicationtimedata_row,chrBasedDecileIndexArray,decileIndex):
    start= chrBased_replicationtimedata_row['start']
    end = chrBased_replicationtimedata_row['end'] + 1
    chrBasedDecileIndexArray[start:end] = decileIndex
##################################################################


##################################################################
def  fillChrBasedDecileIndexArray(chrLong,chrBased_grouped_decile_list):
    #We can set the starring index as 1 in builtin function enumerate
    #First chrBased_grouped_decile has index of 1
    #Last chrBased_grouped_decile has index of 10

    # int8	Byte (-128 to 127)
    chrBasedReplicationTimeDataArrayWithDecileIndex = np.zeros(MAXIMUM_CHROMOSOME_LENGTH, dtype=np.int8)

    #First decileIndex is 1, last decile index is 10.
    for decileIndex, chrBased_grouped_decile in enumerate(chrBased_grouped_decile_list,1):
        if chrLong in chrBased_grouped_decile.groups.keys():
            chrBased_replicationtimedata_df = chrBased_grouped_decile.get_group(chrLong)
            #what is chrBased_decile's type? DataFrame
            if ((chrBased_replicationtimedata_df is not None) and (not chrBased_replicationtimedata_df.empty)):
                chrBased_replicationtimedata_df.apply(fillArray,chrBasedDecileIndexArray=chrBasedReplicationTimeDataArrayWithDecileIndex,decileIndex=decileIndex, axis=1)

    return chrBasedReplicationTimeDataArrayWithDecileIndex
##################################################################



##################################################################
# Case1: SPMS (AGGREGATEDSUBSTITUTIONS and Signatures)
def generateNPArrayAndSearchSubsOnNPArray(inputList):

    chrLong = inputList[0]
    sample2NumberofSubsDict = inputList[1]
    subSignature2NumberofMutationsDict = inputList[2]
    sample2SubsSignature2NumberofMutationsDict = inputList[3]
    chrBased_subs_df_split = inputList[4]
    chrBased_grouped_decile_list = inputList[5]

    #fill nparray slices with decileIndex and return it in the function fillChrBasedDecileIndexArray
    chrBasedReplicationTimeDataArrayWithDecileIndex = fillChrBasedDecileIndexArray(chrLong,chrBased_grouped_decile_list)

    type2DecileIndex2NumberofMutationsDict, sample2Type2DecileIndex2NumberofMutationsDict = searchForSubs(subSignature2NumberofMutationsDict,sample2SubsSignature2NumberofMutationsDict, chrBased_subs_df_split,chrBasedReplicationTimeDataArrayWithDecileIndex)

    return type2DecileIndex2NumberofMutationsDict, sample2Type2DecileIndex2NumberofMutationsDict
##################################################################


##################################################################
#Case3: Indels
def generateNPArrayAndSearchIndelsOnNPArray(inputList):
    chrLong = inputList[0]
    sample2SignaturesWithAtLeast10KEligibleMutations2NumberofMutationsDict = inputList[1]
    chrBased_indels_df_split = inputList[2]
    chrBased_grouped_decile_list = inputList[3]

    #fill nparray slices with decileIndex and return it in the function fillChrBasedDecileIndexArray
    chrBasedReplicationTimeDataArrayWithDecileIndex = fillChrBasedDecileIndexArray(chrLong,chrBased_grouped_decile_list)

    indelType2DecileIndex2NumberofMutationsDict, sample2IndelType2DecileIndex2NumberofMutationsDict = searchForIndels(sample2SignaturesWithAtLeast10KEligibleMutations2NumberofMutationsDict,chrBased_indels_df_split,chrBasedReplicationTimeDataArrayWithDecileIndex)

    return indelType2DecileIndex2NumberofMutationsDict, sample2IndelType2DecileIndex2NumberofMutationsDict
##################################################################



##################################################################
#Case2: SPMs and Indels
def generateNPArrayAndSearchSubsAndIndelsOnNPArray(inputList):

    chrLong = inputList[0]
    sample2NumberofSubs = inputList[1]
    subsSignature2NumberofMutationsDict = inputList[2]
    sample2SubsSignature2NumberofMutationsDict = inputList[3]

    sample2NumberofIndelsDict = inputList[4]
    indelsSignature2NumberofMutationsDict = inputList[5]
    sample2IndelsSignature2NumberofMutationsDict = inputList[6]

    chrBased_subs_df_split = inputList[7]
    chrBased_indels_df_split = inputList[8]
    chrBased_grouped_decile_list = inputList[9]

    #fill nparray slices with decileIndex and return it in the function fillChrBasedDecileIndexArray
    chrBasedReplicationTimeDataArrayWithDecileIndex = fillChrBasedDecileIndexArray(chrLong,chrBased_grouped_decile_list)

    type2DecileIndex2NumberofMutationsDict, sample2Type2DecileIndex2NumberofMutationsDict = searchForSubs(
        subsSignature2NumberofMutationsDict,
        sample2SubsSignature2NumberofMutationsDict,
        chrBased_subs_df_split,
        chrBasedReplicationTimeDataArrayWithDecileIndex)

    indelType2DecileIndex2NumberofMutationsDict, sample2IndelType2DecileIndex2NumberofMutationsDict = searchForIndels(
        sample2IndelsSignature2NumberofMutationsDict,
        chrBased_indels_df_split,
        chrBasedReplicationTimeDataArrayWithDecileIndex)

    #Update type2DecileIndex2NumberofMutationsDict with indelType2DecileIndex2NumberofMutationsDict
    type2DecileIndex2NumberofMutationsDict.update(indelType2DecileIndex2NumberofMutationsDict)

    #Update sample2SPMType2DecileIndex2NumberofMutationsDict with sample2IndelType2DecileIndex2NumberofMutationsDict
    #Since types are not overlapping.
    for sample in sample2IndelType2DecileIndex2NumberofMutationsDict:
        if sample in sample2Type2DecileIndex2NumberofMutationsDict:
            sample2Type2DecileIndex2NumberofMutationsDict[sample].update(sample2IndelType2DecileIndex2NumberofMutationsDict[sample])
        else:
            sample2Type2DecileIndex2NumberofMutationsDict[sample]  = sample2IndelType2DecileIndex2NumberofMutationsDict[sample]


    #TODO question can we update two level dictionaries using built in update method?
    # Answer: No. It overwrites for the first level keys
    # Answer: It can used when keys are not overlapping.

    return type2DecileIndex2NumberofMutationsDict, sample2Type2DecileIndex2NumberofMutationsDict
##################################################################



##################################################################
#Accumulate the counts coming from each chromosome split in type2DecileBasedAllChrAccumulatedCountDict and sample2Type2DecileBasedAllChrAccumulatedCountDict
def accumulateTypeBasedDictionariesWithExtraSampleBased(listofDictionaries,type2DecileBasedAllChrAccumulatedCountDict,sample2Type2DecileBasedAllChrAccumulatedCountDict):
    for dictList in listofDictionaries:

        typeBasedDict = dictList[0]
        sampleBasedTypeDict = dictList[1]

        # ############################################################################
        # print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
        # print('These 2 dictionaries will be accumulated. Are they full?')
        # print('typeBasedDict')
        # print(typeBasedDict)
        # print('sampleBasedTypeDict')
        # print(sampleBasedTypeDict)
        # print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
        # ############################################################################

        ###########################################################################
        for type, decileBasedAllChrAccumulatedCountDict in typeBasedDict.items():

            if type not in type2DecileBasedAllChrAccumulatedCountDict:
                type2DecileBasedAllChrAccumulatedCountDict[type] = {}

            tobeUpdatedDecileBasedAllChrAccumulatedCountDict=  type2DecileBasedAllChrAccumulatedCountDict[type]

            for decileIndex, decileCount in decileBasedAllChrAccumulatedCountDict.items():
                #if key in dictionary
                if decileIndex in tobeUpdatedDecileBasedAllChrAccumulatedCountDict:
                    tobeUpdatedDecileBasedAllChrAccumulatedCountDict[decileIndex] += decileCount
                else:
                    tobeUpdatedDecileBasedAllChrAccumulatedCountDict[decileIndex] = decileCount
        ###########################################################################

        ######################## Sample Based starts #######################################
        for sample in sampleBasedTypeDict:
            if sample not in sample2Type2DecileBasedAllChrAccumulatedCountDict:
                sample2Type2DecileBasedAllChrAccumulatedCountDict[sample] = {}

            #left here I guess I found what is missing?
            for type, decileBasedAllChrAccumulatedCountDict in sampleBasedTypeDict[sample].items():
                if type not in sample2Type2DecileBasedAllChrAccumulatedCountDict[sample]:
                    sample2Type2DecileBasedAllChrAccumulatedCountDict[sample][type] = {}

                tobeUpdatedDecileBasedAllChrAccumulatedCountDict = sample2Type2DecileBasedAllChrAccumulatedCountDict[sample][type]

                for decileIndex, decileCount in decileBasedAllChrAccumulatedCountDict.items():
                    # if key in dictionary
                    if decileIndex in tobeUpdatedDecileBasedAllChrAccumulatedCountDict:
                        tobeUpdatedDecileBasedAllChrAccumulatedCountDict[decileIndex] += decileCount
                    else:
                        tobeUpdatedDecileBasedAllChrAccumulatedCountDict[decileIndex] = decileCount
        ######################## Sample Based ends #########################################

##################################################################


##################################################################
def getNormalizedMutationDensityList(mutationDensityDict):
    densities = mutationDensityDict.values()
    maxDensity = max(densities)
    if maxDensity>0:
        normalizedMutationDensities = [x/maxDensity for x in densities]

    else:
        normalizedMutationDensities = densities

    return normalizedMutationDensities
##################################################################


##################################################################
def getMutationDensityDict(deciles,decileBasedAllChrAccumulatedCountDict):
    decileBasedMutationDensityDict = {}
    numberofMutations = 0


    #Modifiled as enumerate(deciles,1) formerly it was enumerate(deciles,0)
    for i,decile in enumerate(deciles,1):
        if (i in decileBasedAllChrAccumulatedCountDict):
            count = decileBasedAllChrAccumulatedCountDict[i]
            numberofMutations += count
            numofAttBases = decile['numofBases'].sum()
            mutationDensity=float(count)/numofAttBases
            decileBasedMutationDensityDict[i] = mutationDensity
        else:
            decileBasedMutationDensityDict[i] = 0

        # print('decile: %d numofAttBases: %d' %(i,numofAttBases))

    return numberofMutations, decileBasedMutationDensityDict
##################################################################


##################################################################
def calculateCountsForSubsAndIndels(outputDir,jobname,numofProcesses,pool,
                                    sample2NumberofSubsDict,
                                    subsSignature2NumberofMutationsDict,
                                    sample2SubsSignature2NumberofMutationsDict,
                                    sample2NumberofIndelsDict,
                                    indelsSignature2NumberofMutationsDict,
                                    sample2IndelsSignature2NumberofMutationsDict,
                                    deciles,
                                    chrNamesInReplicationTimeDataList,
                                    singlePointMutationsFileName,
                                    indelsFilename):

    type2DecileBasedAllChrAccumulatedCountDict = {}
    sample2Type2DecileBasedAllChrAccumulatedCountDict ={}

    #Get chrBased grouped deciles
    chrBased_grouped_decile_list = []
    #Get this chrLong of each decile
    #The first decile is the earliest one with index 1
    #The last decile is the latest one with index 10
    #We provide these indexes later in the fillChrBasedDecileIndexArray function by enumerate
    for decile in deciles:
        chrBased_grouped_decile = decile.groupby('chr')
        chrBased_grouped_decile_list.append(chrBased_grouped_decile)

    #It seems that chrNames in replicationTimeData are long chr names such as chr1, chrX
    for chrLong in chrNamesInReplicationTimeDataList:
        # chrLong = 'chr%s' %(chr)

        chrBased_subs_df = readChrBasedMutationDF(outputDir,jobname,chrLong,singlePointMutationsFileName)
        chrBased_indels_df = readChrBasedIndelsDF(outputDir,jobname,chrLong,indelsFilename)

        ###################################################################################################################################################
        if (((chrBased_subs_df is not None) and  (not chrBased_subs_df.empty))  and ((chrBased_indels_df is not None) and (not chrBased_indels_df.empty)) ):

            chrBased_subs_df_splits = np.array_split(chrBased_subs_df, numofProcesses)
            chrBased_indels_df_splits = np.array_split(chrBased_indels_df,numofProcesses)
            zipped = zip(chrBased_subs_df_splits,chrBased_indels_df_splits)

            poolInputList = []
            for zippedTuple in zipped:
                inputList = []
                inputList.append(chrLong) #Same
                inputList.append(sample2NumberofSubsDict)
                inputList.append(subsSignature2NumberofMutationsDict)
                inputList.append(sample2SubsSignature2NumberofMutationsDict)
                inputList.append(sample2NumberofIndelsDict)
                inputList.append(indelsSignature2NumberofMutationsDict)
                inputList.append(sample2IndelsSignature2NumberofMutationsDict)
                chrBased_subs_df_split= zippedTuple[0]
                chrBased_indels_df_split = zippedTuple[1]
                inputList.append(chrBased_subs_df_split) #Different
                inputList.append(chrBased_indels_df_split) #Different
                inputList.append(chrBased_grouped_decile_list)  #Same
                poolInputList.append(inputList)

            # Call the parallel code for poolInputList
            # It returns a list of whatever generateNPArrayAndSearchMutationsOnNPArray will return
            # It must return list of tuples
            # Since generateNPArrayAndSearchMutationsOnNPArray return tuple
            # Fill np.array with 0 if there is no signal, otherwise fill with the decileIndex if there is a signal
            listofDictionaries = pool.map(generateNPArrayAndSearchSubsAndIndelsOnNPArray,poolInputList)

            accumulateTypeBasedDictionariesWithExtraSampleBased(listofDictionaries,type2DecileBasedAllChrAccumulatedCountDict,sample2Type2DecileBasedAllChrAccumulatedCountDict)
        ###################################################################################################################################################

        ###################################################################################################################################################
        elif ((chrBased_subs_df is not None) and (not chrBased_subs_df.empty)):
            #split chrBased_mutation_df as many as number of cores
            chrBased_mutation_df_splits = np.array_split(chrBased_subs_df,numofProcesses)

            poolInputList = []
            for chrBased_mutation_df_split in chrBased_mutation_df_splits:
                inputList = []
                inputList.append(chrLong) #Same
                inputList.append(sample2NumberofSubsDict)
                inputList.append(subsSignature2NumberofMutationsDict) #same
                inputList.append(sample2SubsSignature2NumberofMutationsDict) #same
                inputList.append(chrBased_mutation_df_split) #Different
                inputList.append(chrBased_grouped_decile_list) #Same
                poolInputList.append(inputList)

            # Call the parallel code for poolInputList
            # It returns a list of whatever generateNPArrayAndSearchMutationsOnNPArray will return
            # It must return list of tuples
            # Since generateNPArrayAndSearchMutationsOnNPArray return tuple
            # Fill np.array with 0 if there is no signal, otherwise fill with the decileIndex if there is a signal
            # pool.map blocks until the result is ready.
            listofDictionaries = pool.map(generateNPArrayAndSearchSubsOnNPArray,poolInputList)

            accumulateTypeBasedDictionariesWithExtraSampleBased(listofDictionaries,type2DecileBasedAllChrAccumulatedCountDict,sample2Type2DecileBasedAllChrAccumulatedCountDict)


        ###################################################################################################################################################

        ###################################################################################################################################################
        elif ((chrBased_indels_df is not None) and (not chrBased_indels_df.empty)):
            # split chrBased_indels_df as many as number of cores
            chrBased_indels_df_splits = np.array_split(chrBased_indels_df,numofProcesses)

            poolInputList = []
            for chrBased_indels_df_split  in chrBased_indels_df_splits:
                inputList = []
                inputList.append(chrLong) #Same
                inputList.append(sample2SubsSignature2NumberofMutationsDict)
                inputList.append(chrBased_indels_df_split) #Different
                inputList.append(chrBased_grouped_decile_list) #Same
                poolInputList.append(inputList)

            # Call the parallel code for poolInputList
            # It returns a list of whatever generateNPArrayAndSearchMutationsOnNPArray will return
            # It must return list of tuples
            # Since generateNPArrayAndSearchMutationsOnNPArray return tuple
            # Fill np.array with 0 if there is no signal, otherwise fill with the decileIndex if there is a signal
            listofDictionaries = pool.map(generateNPArrayAndSearchIndelsOnNPArray,poolInputList)

            #Accumulate listofTuples coming from each chromosome in type2DecileBasedAllChrAccumulatedCountDict
            #TODO here there are two dictionaries
            accumulateTypeBasedDictionariesWithExtraSampleBased(listofDictionaries,type2DecileBasedAllChrAccumulatedCountDict,sample2Type2DecileBasedAllChrAccumulatedCountDict)
        ###################################################################################################################################################

    return type2DecileBasedAllChrAccumulatedCountDict, sample2Type2DecileBasedAllChrAccumulatedCountDict

##################################################################



##################################################################
def augment(pool,wavelet_processed_df,genome):
    if (genome==GRCh37):
        genome = twobitreader.TwoBitFile(os.path.join(current_abs_path,ONE_DIRECTORY_UP,ONE_DIRECTORY_UP,LIB,UCSCGENOME,HG19_2BIT))
    elif (genome==GRCh38):
        genome = twobitreader.TwoBitFile(os.path.join(current_abs_path,ONE_DIRECTORY_UP,ONE_DIRECTORY_UP,LIB,UCSCGENOME,HG38_2BIT))

    #Augment in parallel for each chromosome
    poolInputList = []
    chrBased_wavelet_processed_df_groups = wavelet_processed_df.groupby('chr')
    for chr, chrBased_wavelet_processed_df_group in chrBased_wavelet_processed_df_groups:
        inputList = []
        inputList.append(chr)
        inputList.append(chrBased_wavelet_processed_df_group)
        #Please note that when you provide the chr based hg19_genome it gives error
        inputList.append(genome)
        poolInputList.append(inputList)

    # print('Augmentation starts')
    #Each tuple contains chrLong and the dataframe with augmented column with number of attributable bases
    listofTuples = pool.map(addNumofAttributableBasesColumn,poolInputList)
    # print('len(poolInputList): %d' %len(poolInputList))
    # print('len(listofDFs): %d' %len(listofTuples))

    #Define frames which will be a list of dataframes
    #columns = ['chr','start','end','signal','numofBases']
    #augment_df = pd.DataFrame(columns=columns)
    frames = []

    for tuple in listofTuples:
        #chrLong = tuple[0]
        chrBased_augmented_df = tuple[1]
        frames.append(chrBased_augmented_df)

    augment_df = pd.concat(frames,ignore_index=True)

    # print('##### augmented_df description starts #####################')
    # print(augment_df.columns.values.tolist())
    # print(type(augment_df))
    # print(len(augment_df))
    # print('##### augmented_df description ends #####################')
    # print('augment ends')

    return augment_df
##################################################################




##################################################################
#Case 1: SPMS  (AGGREGATEDSUBSTITUTIONS and Signatures)
def writeReplicationTimeDataForSPMsWithExtraSampleBased(outputDir,jobname,deciles,type2DecileBasedAllChrAccumulatedCountDict,sample2Type2DecileBasedAllChrAccumulatedCountDict):
    os.makedirs(os.path.join(outputDir, jobname, DATA, REPLICATIONTIME,'normalized_mutation_density'), exist_ok=True)

    #One of the type is AGGREGATEDSUBSTITUTIONS

    ##############################################################
    for type in type2DecileBasedAllChrAccumulatedCountDict:
        decileBasedAllChrAccumulatedCountDict = type2DecileBasedAllChrAccumulatedCountDict[type]

        normalizedMutationDensityFilename = type + '_NormalizedMutationDensity.txt'
        normalizedMutationDensityFilePath = os.path.join(outputDir,jobname, DATA, REPLICATIONTIME, 'normalized_mutation_density',
                                                         normalizedMutationDensityFilename)

        # If decileBasedAllChrAccumulatedCountDict is not empty
        if (decileBasedAllChrAccumulatedCountDict):
            numberofMutations, mutationDensityDict = getMutationDensityDict(deciles,decileBasedAllChrAccumulatedCountDict)
            normalizedMutationDensityList = getNormalizedMutationDensityList(mutationDensityDict)

            with open(normalizedMutationDensityFilePath, 'w') as file:
                for normalizedMutationDensity in normalizedMutationDensityList:
                    file.write(str(normalizedMutationDensity) + ' ')
                file.write('\n')
    ##############################################################

    ######################### Sample Based starts #####################
    for sample in sample2Type2DecileBasedAllChrAccumulatedCountDict:
        for type in sample2Type2DecileBasedAllChrAccumulatedCountDict[sample]:
            decileBasedAllChrAccumulatedCountDict = sample2Type2DecileBasedAllChrAccumulatedCountDict[sample][type]

            normalizedMutationDensityFilename = '%s_%s_NormalizedMutationDensity.txt' %(sample,type)
            normalizedMutationDensityFilePath = os.path.join(outputDir,jobname, DATA, REPLICATIONTIME, 'normalized_mutation_density',
                                                             normalizedMutationDensityFilename)

            #If decileBasedAllChrAccumulatedCountDict is not empty
            if (decileBasedAllChrAccumulatedCountDict):
                numberofMutations, mutationDensityDict = getMutationDensityDict(deciles, decileBasedAllChrAccumulatedCountDict)
                normalizedMutationDensityList = getNormalizedMutationDensityList(mutationDensityDict)

                with open(normalizedMutationDensityFilePath, 'w') as file:
                    for normalizedMutationDensity in normalizedMutationDensityList:
                        file.write(str(normalizedMutationDensity) + ' ')
                    file.write('\n')
    ######################### Sample Based ends #######################

##################################################################


##################################################################
def replicationTimeAnalysis(genome,outputDir,jobname,singlePointMutationsFileName,indelsFilename,repliseqDataFilename):

    print('########################## ReplicationTimeAnalysis starts #########################')
    #########################################################################
    # Analysis Type can be
    # AggregatedSubstitutions: All in one
    # AggregatedIndels : All in one
    # IndelsBased : Microhomology, Repeat
    # SignatureBased: Sig1, Sig2, ...

    # We know the indels type we are interested in.
    # Microhomology indels --- len(indels) >= 3
    # Repeat indels --- len(indels) < 3
    # indeltypes = [MICROHOMOLOGY, REPEAT]
    #########################################################################

    numofProcesses = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(numofProcesses)

    ###################################################################
    ############### Read MCF-7 RepliSeq Time data starts ##############
    ###################################################################
    chrNamesInReplicationTimeDataArray, deciles = readRepliSeqTimeData(pool,repliseqDataFilename,genome)
    chrNamesInReplicationTimeDataList = chrNamesInReplicationTimeDataArray.tolist()
    #What is the type of deciles? Deciles is a list of dataframes.
    ###################################################################
    ############### Read MCF-7 RepliSeq Time data ends ################
    ###################################################################


    ##########################################################################################
    sample2NumberofSubsDict = getSample2NumberofSubsDict(outputDir,jobname)
    sample2NumberofIndelsDict = getSample2NumberofIndelsDict(outputDir,jobname)

    subsSignature2NumberofMutationsDict = getSubsSignature2NumberofMutationsDict(outputDir,jobname)
    indelsSignature2NumberofMutationsDict = getIndelsSignature2NumberofMutationsDict(outputDir, jobname)

    sample2SubsSignature2NumberofMutationsDict = getSample2SubsSignature2NumberofMutationsDict(outputDir,jobname)
    sample2IndelsSignature2NumberofMutationsDict = getSample2IndelsSignature2NumberofMutationsDict(outputDir,jobname)
    ##########################################################################################


    #######################################################################################################
    ############### Carry out Replication Time Data Analysis for each analysis type starts ################
    #######################################################################################################
    type2DecileBasedAllChrAccumulatedCountDict , sample2Type2DecileBasedAllChrAccumulatedCountDict = calculateCountsForSubsAndIndels(
                                                                                                                            outputDir,jobname,numofProcesses,pool,
                                                                                                                            sample2NumberofSubsDict,
                                                                                                                            subsSignature2NumberofMutationsDict,
                                                                                                                            sample2SubsSignature2NumberofMutationsDict,
                                                                                                                            sample2NumberofIndelsDict,
                                                                                                                            indelsSignature2NumberofMutationsDict,
                                                                                                                            sample2IndelsSignature2NumberofMutationsDict,
                                                                                                                            deciles,
                                                                                                                            chrNamesInReplicationTimeDataList,
                                                                                                                            singlePointMutationsFileName,
                                                                                                                            indelsFilename)

    writeReplicationTimeDataForSPMsWithExtraSampleBased(outputDir,jobname,deciles,type2DecileBasedAllChrAccumulatedCountDict,sample2Type2DecileBasedAllChrAccumulatedCountDict)

    ################################
    pool.close()
    pool.join()
    ################################

    print('########################## ReplicationTimeAnalysis ends ############################')

##################################################################