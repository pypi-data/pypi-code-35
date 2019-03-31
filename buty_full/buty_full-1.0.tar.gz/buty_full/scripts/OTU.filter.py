import os
from Bio import SeqIO
import argparse
import glob
import pandas as pd
import numpy as np

############################################ Arguments and declarations ##############################################
parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("-t",
                    help="file name of your otu_table", type=str, default='a.otu.table',metavar='a.otu.table')
parser.add_argument("-s",
                    help="file name of your otu_seq", type=str, default='a.otu.fasta',metavar='a.otu.fasta')
parser.add_argument("-r",
                    help="results_dir", type=str, default='Filtered_OTU',metavar='Filtered_OTU')
parser.add_argument("-top",
                    help="number of top OTUs", type=int, default=5000,metavar=5000)


################################################## Definition ########################################################
args = parser.parse_args()
try:
    os.mkdir(args.r)
except OSError:
    pass


################################################### Function ########################################################
def Maxabu(Abus):
    Abumax=0
    for number in Abus:
        Abumax=max(Abumax, int(number.replace('\r','').replace('\n','')))
    return Abumax


def Tableinput(otutablefile,topnumber):
    OTUtable=dict()
    OTUtop=[]
    rootofutb, otutable = os.path.split(otutablefile)
    OTU_table = pd.read_csv(otutablefile, sep='\t', index_col=0)
    #OTU_table['sum']=OTU_table.sum(axis=0,numeric_only=True)
    OTU_table_new=OTU_table.div(OTU_table.sum(axis=0,numeric_only=True), axis=1)
    OTU_table_new.to_csv(os.path.join(args.r,otutable+'.abu.table'), sep='\t', header=True)
    Abus=OTU_table_new.max(axis=1,numeric_only=True).tolist()
    i=0
    for OTUs in OTU_table_new.index:
        OTUtable.setdefault(OTUs,Abus[i])
        i+=1
    Abus.sort(reverse=True)
    f1 = open(os.path.join(args.r,otutable+'.max.abu'),'w')
    for OTUs in OTUtable:
        if OTUtable[OTUs] >= Abus[topnumber-1] and OTUtable[OTUs] >= 0.00001:
            f1.write(str(OTUs)+'\t'+str(OTUtable[OTUs])+'\n')
            OTUtop.append(OTUs)
    f1.close()
    return OTUtop


def Tableoutput(OTUtop,otuseqfile):
    rootofus, otuseq = os.path.split(otuseqfile)
    f1 = open(os.path.join(args.r,otuseq+'.filter'),'w')
    for record in SeqIO.parse(open(otuseqfile, 'r'), 'fasta'):
        if record.id in OTUtop:
            f1.write('>' + str(record.id) + '\n' + str(str(record.seq)) + '\n')
################################################### Programme #######################################################
Tableoutput(Tableinput(args.t,args.top),args.s)
