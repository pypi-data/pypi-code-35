import os
from Bio import SeqIO
import argparse
import glob
import pandas as pd
import numpy as np



############################################ Arguments and declarations ##############################################
parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("-t",
                    help="file name of your tree", type=str, default='16S.nwk',metavar='16S.nwk')
parser.add_argument("-n",
                    help="file name of your tree node names", type=str, default='16S.format.name',metavar='16S.format.name')
parser.add_argument("-rd",
                    help="the reference data of gene traits", type=str, default='Data.txt',metavar='Data.txt')
parser.add_argument("-a",
                    help="file name of your otu abundance", type=str, default='abu.table',metavar='abu.table')
parser.add_argument("-r",
                    help="results_dir", type=str, default='Bayers_model',metavar='Bayers_model')
parser.add_argument("-b",
                    help="dir to inferTraits tool", type=str,
                    default='inferTraits.py',
                    metavar='inferTraits.py')


################################################## Definition ########################################################
args = parser.parse_args()
try:
    os.mkdir(args.r)
except OSError:
    pass


################################################### Function ########################################################
def Traitspredicting(filename):
    Tempdf = pd.read_csv(filename, sep='\t',index_col=0,header=None)
    OTUwithTraits=dict()
    for OTUs in Tempdf.index:
        OTUwithTraits.setdefault(OTUs,float(Tempdf.loc[OTUs]))
    OTU_table = pd.read_csv(args.a, sep='\t')
    Newrow = ['Abu_with_Traits']
    Newrow = Newrow + [0]*(len(OTU_table.columns)-1)
    OTU_table.loc[-1] = Newrow
    OTU_table.set_index(OTU_table.columns[0],inplace=True)
    # abundance times butyrate producing score
    for OTUs in OTU_table.index:
        try:
            OTU_table.loc[OTUs] = OTU_table.loc[OTUs]*OTUwithTraits[OTUs]
        except KeyError:
            # OTUs with low abundance that are filtered out
            OTU_table.loc[OTUs] = OTU_table.loc[OTUs] * 0.0
    # calculate total abundance of butyrate producing OTUs
    for OTUs in OTU_table.index:
        try:
            if OTUs != 'Abu_with_Traits':
                OTU_table.loc['Abu_with_Traits'] += OTU_table.loc[OTUs]
        except KeyError:
            pass
    Newrow = OTU_table.loc['Abu_with_Traits']
    OTU_table[0:-1].to_csv(os.path.join(args.r, treefile + '.infertraits.otu_table'),
                                                     sep='\t', header=True)
    Newrow.to_csv(os.path.join(args.r, treefile + '.infertraits.abu'), sep='\t',
                                                       header=True)


################################################### Programme #######################################################
rootofus, treefile = os.path.split(args.t)
os.system('python '+args.b+' -t ' + str(args.t) + ' -n ' + \
           str(args.n)+' -rd ' + \
           str(args.rd) +' -r ' \
           + str(args.r) )
Traitspredicting(os.path.join(args.r,treefile+'.infertraits.txt'))
