# This source code file is a part of SigProfilerTopography
# SigProfilerTopography is a tool included as part of the SigProfiler
# computational framework for comprehensive analysis of mutational
# signatures from next-generation sequencing of cancer genomes.
# SigProfilerTopography provides the downstream data analysis of
# mutations and extracted mutational signatures w.r.t.
# nucleosome occupancy, replication time and strand bias.
# Copyright (C) 2018 Burcak Otlu

###################################################################################
################ This python code read the nucleosome occupancy filename ##########
######################## Remove the outliers or not ###############################
###### Write the chromosome based average nucleosome occupancy signal arrays ######
###################################################################################

#unnesting requires too much memory because of that jobs sleep and then become zombie
import os
import matplotlib
import sys
from sys import getsizeof

BACKEND = 'Agg'
if matplotlib.get_backend().lower() != BACKEND.lower():
    # If backend is not set properly a call to describe will hang
    matplotlib.use(BACKEND)

from matplotlib import pyplot as plt
#To plot for bi range of x axis such as 250M
plt.rcParams['agg.path.chunksize'] = 10000

#############################################################
current_abs_path = os.path.abspath(os.path.dirname(__file__))
#############################################################

commonsPath = os.path.join(current_abs_path, '..','commons')
sys.path.append(commonsPath)

from TopographyCommons import *

#########################################################################
def unnesting(df, explode):
    idx=df.index.repeat(df[explode[0]].str.len())
    df1=pd.concat([pd.DataFrame({x:np.concatenate(df[x].values)} )for x in explode],axis=1)
    df1.index=idx
    return df1.join(df.drop(explode,1),how='left')
#########################################################################



######################################################################
# Requires too much memory results in first sleeping and then zombie jobs
def computeSignalArrayAndCountArray(chromSize,chrBased_nucleosome_df):

    print('for debug in computeSignalArrayAndCountArrayForEachChr starts')
    print('before key column added')
    print('getsizeof(chrBased_nucleosome_df): %d in MB' %int(getsizeof(chrBased_nucleosome_df)/1000000))

    chrBased_nucleosome_df['key'] = [list(range(x, y)) for x, y in zip(chrBased_nucleosome_df.start, chrBased_nucleosome_df.end)]
    print('after key column added')
    print('getsizeof(chrBased_nucleosome_df): %d in MB' %int(getsizeof(chrBased_nucleosome_df)/1000000))

    chrBased_nucleosome_df.drop(['start','end'], axis=1, inplace=True)
    print('after drop column')
    print('getsizeof(chrBased_nucleosome_df): %d in MB' %int(getsizeof(chrBased_nucleosome_df)/1000000))

    # Unnest and  generate signalArray and countArray
    chrBasedNucleosomeDFSignalArray = unnesting(chrBased_nucleosome_df,['key']).groupby('key').signal.sum().reindex(list(range(chromSize))).fillna(0).values
    chrBasedNucleosomeDFCountArray = unnesting(chrBased_nucleosome_df,['key']).groupby('key').signal.count().reindex(list(range(chromSize))).fillna(0).values

    print('getsizeof(chrBasedNucleosomeDFSignalArray): %d MB' %int(getsizeof(chrBasedNucleosomeDFSignalArray)/1000000))
    print('getsizeof(chrBasedNucleosomeDFCountArray): %d MB' %int(getsizeof(chrBasedNucleosomeDFCountArray)/1000000))
    print('np.sum(chrBasedNucleosomeDFSignalArray)')
    print(np.sum(chrBasedNucleosomeDFSignalArray, dtype=np.float64))
    print('np.sum(chrBasedNucleosomeDFCountArray)')
    print(np.sum(chrBasedNucleosomeDFCountArray, dtype=np.float64))
    print('for debug in computeSignalArrayAndCountArrayForEachChr ends')
    return chrBasedNucleosomeDFSignalArray, chrBasedNucleosomeDFCountArray
######################################################################




######################################################################
#Does not work, they sleeps do not run
def  writeChrBasedNucleosomeOccupancySignalCountArrays(chrLong, chromSize, chrBasedNuclesomeDF,nucleosomeFilename):

    numofProcesses = multiprocessing.cpu_count()
    modifiedNumofProcesses = int(numofProcesses/2)

    print('for debug chrLong:%s chrSize:%d' %(chrLong,chromSize))
    os.makedirs(os.path.join(current_abs_path,ONE_DIRECTORY_UP,ONE_DIRECTORY_UP,LIB,NUCLEOSOME,CHRBASED), exist_ok=True)

    print('writeChrBasedNucleosome:%s for %s starts' %(nucleosomeFilename,chrLong))
    nucleosomeFilenameWoExtension = nucleosomeFilename[0:-4]

    signalArrayFilename = '%s_signal_%s' %(chrLong,nucleosomeFilenameWoExtension)
    countArrayFilename = '%s_count_%s' % (chrLong, nucleosomeFilenameWoExtension)

    chrBasedSignalNucleosmeFile = os.path.join(current_abs_path,ONE_DIRECTORY_UP,ONE_DIRECTORY_UP,LIB,NUCLEOSOME,CHRBASED,signalArrayFilename)
    chrBasedCountNucleosmeFile = os.path.join(current_abs_path,ONE_DIRECTORY_UP,ONE_DIRECTORY_UP,LIB,NUCLEOSOME,CHRBASED,countArrayFilename)

    accumulatedSignalArray = np.zeros(chromSize,dtype=np.float32)
    accumulatedCountArray = np.zeros(chromSize, dtype=np.float32)

    ################################
    # pool = multiprocessing.Pool(numofProcesses)
    pool = multiprocessing.Pool(modifiedNumofProcesses)
    chrBasedNucleosomeDFSplits = np.array_split(chrBasedNuclesomeDF, modifiedNumofProcesses)
    ################################

    poolInputList = []
    for idx, chrBasedNucleosomeDFSplit in enumerate(chrBasedNucleosomeDFSplits):
        print('for debug for split %d' %(idx))
        print('chromSize')
        print(chromSize)
        inputList = []
        inputList.append(chromSize)
        inputList.append(chrBasedNucleosomeDFSplit)
        poolInputList.append(inputList)

    allSplits_chrBased_SignalArrayAndCountArray_List = pool.map(computeSignalArrayAndCountArray, poolInputList)

    ################################
    pool.close()
    pool.join()
    ################################


    for split_chrBased_SignalArrayAndCountArray_List in allSplits_chrBased_SignalArrayAndCountArray_List:
        print('For debug type(split_chrBased_SignalArrayAndCountArray_List)')
        print(type(split_chrBased_SignalArrayAndCountArray_List))
        signalArray = split_chrBased_SignalArrayAndCountArray_List[0]
        countArray = split_chrBased_SignalArrayAndCountArray_List[1]
        accumulatedSignalArray += signalArray
        accumulatedCountArray += countArray
        # singalArray, countArray = computeSignalArrayAndCountArrayForEachSplit(chromSize,chrBasedNucleosomeDFSplit)

    np.seterr(divide='ignore', invalid='ignore')
    # averageSignalArray = np.divide(accumulatedSignalArray, accumulatedCountArray, dtype=np.float32)
    # np.nan_to_num(averageSignalArray, copy=False)

    #Save as npy
    np.save(chrBasedSignalNucleosmeFile, accumulatedSignalArray)
    np.save(chrBasedCountNucleosmeFile, accumulatedCountArray)

    #Save as txt
    np.savetxt(chrBasedSignalNucleosmeFile, accumulatedSignalArray)
    np.save(chrBasedCountNucleosmeFile, accumulatedCountArray)

    print('writeChrBasedNucleosome:%s for %s ends' % (nucleosomeFilename, chrLong))
######################################################################

######################################################################
def updateSignalCountArrays(nucleosome_row,signalArray,countArray):
    signalArray[nucleosome_row[start]:nucleosome_row[end]] += nucleosome_row[signal]
    countArray[nucleosome_row[start]:nucleosome_row[end]] += 1
######################################################################

######################################################################
def updateSignalArrays(nucleosome_row,signalArray):
    signalArray[nucleosome_row[start]:nucleosome_row[end]] += nucleosome_row[signal]
######################################################################

######################################################################
# This is used right now.
def  writeChrBasedNucleosomeOccupancySignalCountArraysAtOnceInParallel(inputList):
    chrLong = inputList[0]
    chromSize = inputList[1]
    chrBasedNuclesomeDF = inputList[2]
    nucleosomeFilename = inputList[3]

    print('for debug chrLong:%s chrSize:%d' %(chrLong,chromSize))
    os.makedirs(os.path.join(current_abs_path,ONE_DIRECTORY_UP,ONE_DIRECTORY_UP,LIB,NUCLEOSOME,CHRBASED), exist_ok=True)

    print('writeChrBasedNucleosome:%s for %s starts' %(nucleosomeFilename,chrLong))
    nucleosomeFilenameWoExtension = os.path.basename(nucleosomeFilename)[0:-4]

    #Another Way
    signalArray = np.zeros(chromSize,dtype=np.float32)
    # countArray = np.zeros(chromSize,dtype=np.int32)

    # chrBasedNuclesomeDF.apply(updateSignalCountArrays,signalArray=signalArray,countArray=countArray,axis=1)
    chrBasedNuclesomeDF.apply(updateSignalArrays, signalArray=signalArray, axis=1)

    #############################  Save as npy starts ################################
    signalArrayFilename = '%s_signal_%s' %(chrLong,nucleosomeFilenameWoExtension)
    # countArrayFilename = '%s_count_%s' % (chrLong, nucleosomeFilenameWoExtension)

    chrBasedSignalNucleosmeFile = os.path.join(current_abs_path,ONE_DIRECTORY_UP,ONE_DIRECTORY_UP,LIB,NUCLEOSOME,CHRBASED,signalArrayFilename)
    # chrBasedCountNucleosmeFile = os.path.join(current_abs_path,ONE_DIRECTORY_UP,ONE_DIRECTORY_UP,LIB,NUCLEOSOME,CHRBASED,countArrayFilename)

    np.save(chrBasedSignalNucleosmeFile, signalArray)
    # np.save(chrBasedCountNucleosmeFile, countArray)
    #############################  Save as npy ends ##################################

    print('writeChrBasedNucleosome:%s for %s ends' % (nucleosomeFilename, chrLong))
######################################################################


######################################################################
#Not used any more
def  writeChrBasedNucleosomeOccupancySignalCountArraysAtOnce(chrLong, chromSize, chrBasedNuclesomeDF,nucleosomeFilename):

    print('for debug chrLong:%s chrSize:%d' %(chrLong,chromSize))
    os.makedirs(os.path.join(current_abs_path,ONE_DIRECTORY_UP,ONE_DIRECTORY_UP,LIB,NUCLEOSOME,CHRBASED), exist_ok=True)

    print('writeChrBasedNucleosome:%s for %s starts' %(nucleosomeFilename,chrLong))
    nucleosomeFilenameWoExtension = nucleosomeFilename[0:-4]

    accumulatedSignalArray, accumulatedCountArray= computeSignalArrayAndCountArray(chromSize,chrBasedNuclesomeDF)

    #############################  Save as npy starts ################################
    signalArrayFilename = '%s_signal_%s' %(chrLong,nucleosomeFilenameWoExtension)
    countArrayFilename = '%s_count_%s' % (chrLong, nucleosomeFilenameWoExtension)

    chrBasedSignalNucleosmeFile = os.path.join(current_abs_path,ONE_DIRECTORY_UP,ONE_DIRECTORY_UP,LIB,NUCLEOSOME,CHRBASED,signalArrayFilename)
    chrBasedCountNucleosmeFile = os.path.join(current_abs_path,ONE_DIRECTORY_UP,ONE_DIRECTORY_UP,LIB,NUCLEOSOME,CHRBASED,countArrayFilename)

    np.save(chrBasedSignalNucleosmeFile, accumulatedSignalArray)
    np.save(chrBasedCountNucleosmeFile, accumulatedCountArray)
    #############################  Save as npy ends ##################################

    ############################# Save as txt starts #################################
    signalArrayFilename = '%s_signal_%s.txt' %(chrLong,nucleosomeFilenameWoExtension)
    countArrayFilename = '%s_count_%s.txt' % (chrLong, nucleosomeFilenameWoExtension)

    chrBasedSignalNucleosmeFile = os.path.join(current_abs_path,ONE_DIRECTORY_UP,ONE_DIRECTORY_UP,LIB,NUCLEOSOME,CHRBASED,signalArrayFilename)
    chrBasedCountNucleosmeFile = os.path.join(current_abs_path,ONE_DIRECTORY_UP,ONE_DIRECTORY_UP,LIB,NUCLEOSOME,CHRBASED,countArrayFilename)

    np.savetxt(chrBasedSignalNucleosmeFile, accumulatedSignalArray)
    np.savetxt(chrBasedCountNucleosmeFile, accumulatedCountArray)
    ############################# Save as txt ends ###################################

    print('writeChrBasedNucleosome:%s for %s ends' % (nucleosomeFilename, chrLong))
######################################################################


######################################################################
def readChromBasedNucleosomeDF(chrLong,nucleosomeFilename):
    chrBasedNucleosmeFilename = '%s_%s' %(chrLong,nucleosomeFilename)
    chrBasedNucleosmeFilePath = os.path.join(current_abs_path, ONE_DIRECTORY_UP, ONE_DIRECTORY_UP, LIB, NUCLEOSOME, CHRBASED, chrBasedNucleosmeFilename)

    if (os.path.exists(chrBasedNucleosmeFilePath)):
        column_names = [chrom, start, end, signal]
        # chrbased_nucleosome_df = pd.read_table(chrBasedNucleosmeFilePath, sep="\t", header=None, comment='#', names=column_names,dtype={'chrom': str, 'start': np.int32, 'end': np.int32, 'signal': np.float16})
        chrbased_nucleosome_df = pd.read_table(chrBasedNucleosmeFilePath, sep="\t", header=None, comment='#',names=column_names, dtype={chrom: str, start: np.int32, end: np.int32, signal: np.float32})
        return chrbased_nucleosome_df
    else:
        return None
######################################################################

######################################################################
#main function parallel
# parallel it does not end for big chromosomes
def plotChrBasedNucleosomeOccupancyFigures(nucleosomeFilename):
    #read chromnames for this nucleosome data

    nucleosomeFilenameWoExtension = nucleosomeFilename[0:-4]

    ChrNamesFilepath = os.path.join(current_abs_path, ONE_DIRECTORY_UP, ONE_DIRECTORY_UP, LIB, NUCLEOSOME, ChrNamesInNucleosomesFilename)
    print('for debug ChrNamesFilepath: %s:' %(ChrNamesFilepath))

    if (os.path.exists(ChrNamesFilepath)):
        chromNames = np.loadtxt(ChrNamesFilepath,dtype=np.str)

    print('for debug type(chromNames): %s' %type(chromNames))

    #Start the pool
    numofProcesses = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(numofProcesses)

    poolInputList = []
    for chrLong in chromNames:
        chromBasedNucleosomeDF = readChromBasedNucleosomeDF(chrLong,nucleosomeFilename)
        if chromBasedNucleosomeDF is not None:
            inputList = []
            inputList.append(chrLong)
            inputList.append(nucleosomeFilenameWoExtension)
            poolInputList.append(inputList)

    pool.map(plotNucleosomeOccupancySignalCountFiguresInParallel,poolInputList)

    ################################
    pool.close()
    pool.join()
    ################################

######################################################################

######################################################################
#main function sequential
def plotChrBasedNucleosomeOccupancyFiguresSequential(nucleosomeFilename):
    #read chromnames for this nucleosome data

    nucleosomeFilenameWoExtension = nucleosomeFilename[0:-4]

    ChrNamesFilepath = os.path.join(current_abs_path, ONE_DIRECTORY_UP, ONE_DIRECTORY_UP, LIB, NUCLEOSOME, ChrNamesInNucleosomesFilename)
    print('for debug ChrNamesFilepath: %s:' %(ChrNamesFilepath))

    if (os.path.exists(ChrNamesFilepath)):
        chromNames = np.loadtxt(ChrNamesFilepath,dtype=np.str)

    print('for debug type(chromNames): %s' %type(chromNames))

    for chrLong in chromNames:
        #Actually no need for such a check
        chromBasedNucleosomeDF = readChromBasedNucleosomeDF(chrLong,nucleosomeFilename)
        if chromBasedNucleosomeDF is not None:
            inputList = []
            inputList.append(chrLong)
            inputList.append(nucleosomeFilenameWoExtension)
            plotNucleosomeOccupancySignalCountFiguresInParallel(inputList)

######################################################################



######################################################################
#main function
def plotChrBasedNucleosomeOccupancyFiguresFromText(nucleosomeFilename):
    #read chromnames for this nucleosome data

    nucleosomeFilenameWoExtension = nucleosomeFilename[0:-4]

    ChrNamesFilepath = os.path.join(current_abs_path, ONE_DIRECTORY_UP, ONE_DIRECTORY_UP, LIB, NUCLEOSOME, ChrNamesInNucleosomesFilename)
    print('for debug ChrNamesFilepath: %s:' %(ChrNamesFilepath))

    if (os.path.exists(ChrNamesFilepath)):
        chromNames = np.loadtxt(ChrNamesFilepath,dtype=np.str)

    print('for debug type(chromNames): %s' %type(chromNames))

    #Start the pool
    numofProcesses = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(numofProcesses)

    poolInputList = []
    for chrLong in chromNames:
        chromBasedNucleosomeDF = readChromBasedNucleosomeDF(chrLong,nucleosomeFilename)
        if chromBasedNucleosomeDF is not None:
            inputList = []
            inputList.append(chrLong)
            inputList.append(nucleosomeFilenameWoExtension)
            poolInputList.append(inputList)

    pool.map(plotNucleosomeOccupancySignalCountFiguresInParallelFromTextFiles,poolInputList)

    ################################
    pool.close()
    pool.join()
    ################################

######################################################################

######################################################################
def readAllNucleosomeOccupancyDataAndWriteChrBasedSignalCountArrays(genome, quantileValue, nucleosomeFilename):

    chromSizesDict = getChromSizesDict(genome)

    # Start the pool
    numofProcesses = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(numofProcesses)

    # nucleosmeFilePath = os.path.join(current_abs_path, ONE_DIRECTORY_UP, ONE_DIRECTORY_UP, LIB, NUCLEOSOME, nucleosomeFilename)
    column_names = [chrom, start, end, signal]
    if os.path.exists(nucleosomeFilename):
        nucleosome_df = pd.read_table(nucleosomeFilename, sep="\t", header=None, comment='#', names=column_names, dtype={chrom: str, start: np.int32, end: np.int32, signal: np.float32})

        if (quantileValue<1.0):
            #remove the outliers
            q = nucleosome_df[SIGNAL].quantile(quantileValue)
            print('q:%f' % q)
            print('before %d' % (nucleosome_df.shape[0]))
            nucleosome_df = nucleosome_df[nucleosome_df[SIGNAL] < q]

            nucleosome_df_grouped = nucleosome_df.groupby(chrom)

            poolInputList = []

            for chrLong, chromBasedNucleosomeDF in nucleosome_df_grouped:
                    print('for %s write nucleosome signal and count arrats' %(chrLong))
                    chromSize = chromSizesDict[chrLong]
                    inputList = []
                    inputList.append(chrLong)
                    inputList.append(chromSize)
                    inputList.append(chromBasedNucleosomeDF)
                    inputList.append(nucleosomeFilename)
                    poolInputList.append(inputList)

            pool.map(writeChrBasedNucleosomeOccupancySignalCountArraysAtOnceInParallel, poolInputList)

            ################################
            pool.close()
            pool.join()
            ################################

######################################################################


# ######################################################################
# #main function
# #will be depreceated
# def readChrBasedNucleosomeOccupancyDataAndWriteSignalCountArrays(genome,nucleosomeFilename):
#     chromSizesDict = getChromSizesDict(genome)
#
#     #read chromnames for this nucleosome data
#     ChrNamesFilepath = os.path.join(current_abs_path, ONE_DIRECTORY_UP, ONE_DIRECTORY_UP, LIB, NUCLEOSOME, ChrNamesInNucleosomesFilename)
#     print('for debug ChrNamesFilepath: %s:' %(ChrNamesFilepath))
#
#     if (os.path.exists(ChrNamesFilepath)):
#         chromNames = np.loadtxt(ChrNamesFilepath,dtype=np.str)
#
#     print('for debug type(chromNames): %s' %type(chromNames))
#
#     #Start the pool
#     numofProcesses = multiprocessing.cpu_count()
#     pool = multiprocessing.Pool(numofProcesses)
#
#     poolInputList = []
#     for chrLong in chromNames:
#         chromBasedNucleosomeDF = readChromBasedNucleosomeDF(chrLong,nucleosomeFilename)
#         if chromBasedNucleosomeDF is not None:
#             chromSize = chromSizesDict[chrLong]
#             # writeChrBasedNucleosomeOccupancySignalCountArrays(chrLong, chromSize, chromBasedNucleosomeDF,nucleosomeFilename)
#             # writeChrBasedNucleosomeOccupancySignalCountArraysAtOnce(chrLong, chromSize, chromBasedNucleosomeDF,nucleosomeFilename)
#             inputList = []
#             inputList.append(chrLong)
#             inputList.append(chromSize)
#             inputList.append(chromBasedNucleosomeDF)
#             inputList.append(nucleosomeFilename)
#             poolInputList.append(inputList)
#
#     #Close the pool
#     pool.map(writeChrBasedNucleosomeOccupancySignalCountArraysAtOnceInParallel,poolInputList)
#
#     ################################
#     pool.close()
#     pool.join()
#     ################################
#
# ######################################################################

# ######################################################################
# if __name__== "__main__":
#     #Read chrom based nucleosome data and write the average signal array in npy format
#     # readChrBasedNucleosomeOccupancyDataAndWriteSignalCountArrays('hg19','wgEncodeSydhNsomeGm12878Sig.wig')
#     readChrBasedNucleosomeOccupancyDataAndWriteAverageSignalArray('hg19', 'wgEncodeCrgMapabilityAlign100mer.wig')
# #####################################################################



#####################################################################
def plotNucleosomeOccupancySignalCountFiguresInParallelFromTextFiles(inputList):
    chrLong = inputList[0]
    nucleosomeFilenameWoExtension = inputList[1]

    ##############################################################
    signalArrayFilename = '%s_signal_%s.txt' %(chrLong,nucleosomeFilenameWoExtension)
    countArrayFilename = '%s_count_%s.txt' % (chrLong, nucleosomeFilenameWoExtension)

    chrBasedSignalNucleosmeFile = os.path.join(current_abs_path,ONE_DIRECTORY_UP,ONE_DIRECTORY_UP,LIB,NUCLEOSOME,CHRBASED,signalArrayFilename)
    chrBasedCountNucleosmeFile = os.path.join(current_abs_path,ONE_DIRECTORY_UP,ONE_DIRECTORY_UP,LIB,NUCLEOSOME,CHRBASED,countArrayFilename)

    #################################################################################################################
    if (os.path.exists(chrBasedSignalNucleosmeFile) and os.path.exists(chrBasedCountNucleosmeFile)):

        signal_array_txt = np.loadtxt(chrBasedSignalNucleosmeFile)
        count_array_txt = np.loadtxt(chrBasedCountNucleosmeFile)

        fig = plt.figure(figsize=(30, 10), facecolor=None)
        plt.style.use('ggplot')

        figureFilename = '%s_NucleosomeOccupancy_Signal_Count_from_text.png' %(chrLong)
        figureFilepath = os.path.join(current_abs_path, ONE_DIRECTORY_UP, ONE_DIRECTORY_UP, LIB,NUCLEOSOME,CHRBASED,figureFilename)

        # This code makes the background white.
        ax = plt.gca()
        ax.set_facecolor('white')

        # This code puts the edge line
        for edge_i in ['left', 'bottom', 'right', 'top']:
            ax.spines[edge_i].set_edgecolor("black")
            ax.spines[edge_i].set_linewidth(3)


        #All Chrom
        chromSize = signal_array_txt.size
        x = np.arange(0, chromSize, 1)
        signalPlot = plt.plot(x, signal_array_txt, 'black', label='Signal Array', marker='.', zorder=1)
        countPlot = plt.plot(x, count_array_txt, 'red', label='Count Array', marker='.',zorder=1)

        # # Small Portion of Chrom
        # if chrLong == 'chrM':
        #     chromSize = signal_array_txt.size
        #     x = np.arange(0, chromSize, 1)
        #     signalPlot = plt.plot(x, signal_array_txt, 'black', label='Signal Array', linewidth=1,zorder=1)
        #     countPlot = plt.plot(x, count_array_txt, 'red', label='Count Array', linewidth=1,zorder=1)
        # else:
        #     x=np.arange(41100000,41200000,1)
        #     signalPlot = plt.plot(x, signal_array_txt[41100000:41200000], 'black', label='Signal Array', linewidth=1,zorder=1)
        #     countPlot = plt.plot(x, count_array_txt[41100000:41200000], 'red', label='Count Array', linewidth=1,zorder=1)

        print('chr %s' %chrLong)
        print('signal array shape and size')
        print(signal_array_txt.size)
        print(signal_array_txt.shape)
        print('count array shape and size')
        print(count_array_txt.size)
        print(count_array_txt.shape)

        listofLegends = []
        listofLegends.append(signalPlot[0])
        listofLegends.append(countPlot[0])
        plt.legend(loc='upper left', handles=listofLegends, prop={'size': 24}, shadow=False, edgecolor='white',facecolor='white')

        # Put vertical line at x=0
        # plt.axvline(x=0, color='gray', linestyle='--')

        #Put ylim
        plt.ylim((0,10))

        plt.title('For %s' %(chrLong), fontsize=40, fontweight='bold')
        # plt.show()
        fig.savefig(figureFilepath)
        plt.close(fig)
#####################################################################


#####################################################################
def plotNucleosomeOccupancySignalCountFiguresInParallel(inputList):
    chrLong = inputList[0]
    nucleosomeFilenameWoExtension = inputList[1]

    ##############################################################
    signalArrayFilename = '%s_signal_%s.npy' %(chrLong,nucleosomeFilenameWoExtension)
    countArrayFilename = '%s_count_%s.npy' % (chrLong, nucleosomeFilenameWoExtension)

    chrBasedSignalNucleosmeFile = os.path.join(current_abs_path,ONE_DIRECTORY_UP,ONE_DIRECTORY_UP,LIB,NUCLEOSOME,CHRBASED,signalArrayFilename)
    chrBasedCountNucleosmeFile = os.path.join(current_abs_path,ONE_DIRECTORY_UP,ONE_DIRECTORY_UP,LIB,NUCLEOSOME,CHRBASED,countArrayFilename)

    #################################################################################################################
    if (os.path.exists(chrBasedSignalNucleosmeFile) and os.path.exists(chrBasedCountNucleosmeFile)):

        signal_array_npy = np.load(chrBasedSignalNucleosmeFile)
        count_array_npy = np.load(chrBasedCountNucleosmeFile)

        fig = plt.figure(figsize=(30, 10), facecolor=None)
        plt.style.use('ggplot')

        figureFilename = '%s_NucleosomeOccupancy_Signal_Count_from_npy_scatter_allChr.png' %(chrLong)
        figureFilepath = os.path.join(current_abs_path, ONE_DIRECTORY_UP, ONE_DIRECTORY_UP, LIB,NUCLEOSOME,CHRBASED,figureFilename)

        # This code makes the background white.
        ax = plt.gca()
        ax.set_facecolor('white')

        # This code puts the edge line
        for edge_i in ['left', 'bottom', 'right', 'top']:
            ax.spines[edge_i].set_edgecolor("black")
            ax.spines[edge_i].set_linewidth(3)

        #All Chrom
        chromSize = signal_array_npy.size
        x = np.arange(0, chromSize, 1)
        plt.scatter(x, signal_array_npy, color='black', label='Signal Array', zorder=1)
        plt.scatter(x, count_array_npy, color='red', label='Count Array',zorder=1)

        # #Small Portion of Chrom
        # if chrLong == 'chrM':
        #     chromSize = signal_array_npy.size
        #     x = np.arange(0, chromSize, 1)
        #     # signalPlot = plt.plot(x, signal_array_npy, 'black', label='Signal Array', linewidth=1,zorder=1)
        #     # countPlot = plt.plot(x, count_array_npy, 'red', label='Count Array', linewidth=1,zorder=1)
        #     signalPlot = plt.scatter(x, signal_array_npy, color='black', label='Signal Array',zorder=1)
        #     countPlot = plt.scatter(x, count_array_npy, color ='red', label='Count Array',zorder=1)
        # else:
        #     x=np.arange(41100000,41200000,1)
        #     # signalPlot = plt.plot(x, signal_array_npy[41100000:41200000], 'black', label='Signal Array', linewidth=1,zorder=1)
        #     # countPlot = plt.plot(x, count_array_npy[41100000:41200000], 'red', label='Count Array', linewidth=1,zorder=1)
        #     signalPlot = plt.scatter(x, signal_array_npy[41100000:41200000], color='black', label='Signal Array',zorder=1)
        #     countPlot = plt.scatter(x, count_array_npy[41100000:41200000], color='red', label='Count Array',zorder=1)

        print('chr %s' %chrLong)
        print('x shape and size')
        print(x.size)
        print(x.shape)

        print('signal array shape and size')
        print(signal_array_npy.size)
        print(signal_array_npy.shape)

        print('count array shape and size')
        print(count_array_npy.size)
        print(count_array_npy.shape)

        # listofLegends = []
        # listofLegends.append(signalPlot[0])
        # listofLegends.append(countPlot[0])
        # plt.legend(loc='upper left', handles=listofLegends, prop={'size': 24}, shadow=False, edgecolor='white',facecolor='white')

        # Put vertical line at x=0
        # plt.axvline(x=0, color='gray', linestyle='--')

        #Put ylim
        plt.ylim((0,10))

        plt.title('For %s' %(chrLong), fontsize=40, fontweight='bold')
        # plt.show()
        fig.savefig(figureFilepath)
        plt.close(fig)
    #################################################################################################################



#####################################################################
