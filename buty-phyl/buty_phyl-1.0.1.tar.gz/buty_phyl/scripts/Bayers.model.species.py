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
                    help="file name of your tree node names", type=str,
                    default='16S.format.name',metavar='16S.format.name')
parser.add_argument("-rd",
                    help="the reference data of gene traits", type=str,
                    default='Data.txt',metavar='Data.txt')
parser.add_argument("-a",
                    help="file name of your otu abundance", type=str,
                    default='abu.table',metavar='abu.table')
parser.add_argument("-r",
                    help="results_dir", type=str, default='ButyPhyl',
                    metavar='ButyPhyl')
parser.add_argument("-b",
                    help="dir to inferTraits tool", type=str,
                    default='inferTraits.py',
                    metavar='inferTraits.py')
parser.add_argument("--p",
                        help="further seperate the pathogens and commensals", type=str,
                        default='FALSE', metavar='FALSE or TRUE')
parser.add_argument("--s",
                        help="further infer the species", type=str,
                        default='FALSE', metavar='FALSE or TRUE or your own reference species list')

################################################## Definition ########################################################
args = parser.parse_args()
try:
    os.mkdir(args.r)
except OSError:
    pass


################################################### Function ########################################################
def Traitspredicting(filename, pathogen, speciesfile):
    # load traits
    Tempdf = pd.read_csv(filename, sep='\t',index_col=0,header=None)
    OTUwithTraits=dict()
    for OTUs in Tempdf.index:
        OTUwithTraits.setdefault(OTUs,float(Tempdf.loc[OTUs]))
    # set up species info
    Species = dict()
    Speciesall = []
    for lines in open(speciesfile,'r'):
        Species.setdefault(lines.split('\t')[0], lines.replace('\r','').replace('\n','').split('\t')[1:])
        for species in lines.replace('\r','').replace('\n','').split('\t')[1:]:
            if species not in Speciesall:
                Speciesall.append(species)
    if pathogen == 'FALSE':
        # load abu file
        OTU_table = pd.read_csv(args.a, sep='\t')
        Newrow = ['Abu_with_Traits']
        Newrow = Newrow + [0] * (len(OTU_table.columns) - 1)
        OTU_table.loc[-1] = Newrow
        OTU_table.set_index(OTU_table.columns[0], inplace=True)
        # set up species matrix
        Sprow = pd.DataFrame([[0] * (len(OTU_table.columns))], index=['species'],columns=OTU_table.columns)
        for species in Speciesall:
            Newrow = pd.DataFrame([[0] * (len(OTU_table.columns))], index=[species], columns=OTU_table.columns)
            Sprow=Sprow.append(Newrow)
        # set up butyrate producing species matrix
        Sprowbpb = pd.DataFrame([[0] * (len(OTU_table.columns))], index=['species'], columns=OTU_table.columns)
        for species in Speciesall:
            Newrow = pd.DataFrame([[0] * (len(OTU_table.columns))], index=[species], columns=OTU_table.columns)
            Sprowbpb=Sprowbpb.append(Newrow)
        # abundance times butyrate producing score
        for OTUs in OTU_table.index:
            try:
                # calculate species abundance
                # calculate bpb species abundance
                for species in Species[OTUs]:
                    Sprow.loc[species] += OTU_table.loc[OTUs]
                    Sprowbpb.loc[species] += OTU_table.loc[OTUs] * OTUwithTraits[OTUs]
            except KeyError:
                pass
            try:
                OTU_table.loc[OTUs] = OTU_table.loc[OTUs] * OTUwithTraits[OTUs]
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
        Sprow.to_csv(os.path.join(args.r, treefile + '.species.abu'), sep='\t',
                      header=True)
        Sprowbpb.to_csv(os.path.join(args.r, treefile + '.bpbspecies.abu'), sep='\t',
                      header=True)
    else:
        # load traits of pathogen
        Tempdfpathogen = pd.read_csv(pathogen, sep='\t', index_col=0, header=None)
        OTUwithPathogenTraits = dict()
        for OTUs in Tempdfpathogen.index:
            OTUwithPathogenTraits.setdefault(OTUs, float(Tempdfpathogen.loc[OTUs]))
        # load pathogen abu file
        OTU_table_pathogen = pd.read_csv(args.a, sep='\t')
        Newrow = ['Abu_with_Traits']
        Newrow = Newrow + [0] * (len(OTU_table_pathogen.columns) - 1)
        OTU_table_pathogen.loc[-1] = Newrow
        OTU_table_pathogen.set_index(OTU_table_pathogen.columns[0], inplace=True)
        # load commensal abu file
        OTU_table_commensal = pd.read_csv(args.a, sep='\t')
        Newrow = ['Abu_with_Traits']
        Newrow = Newrow + [0] * (len(OTU_table_commensal.columns) - 1)
        OTU_table_commensal.loc[-1] = Newrow
        OTU_table_commensal.set_index(OTU_table_commensal.columns[0], inplace=True)
        # set up species matrix
        Sprow = pd.DataFrame([[0] * (len(OTU_table.columns))], index=['species'], columns=OTU_table.columns)
        for species in Speciesall:
            Newrow = pd.DataFrame([[0] * (len(OTU_table.columns))], index=[species], columns=OTU_table.columns)
            Sprow = Sprow.append(Newrow)
        # set up pathogen butyrate producing species matrix
        Sprowbpb = pd.DataFrame([[0] * (len(OTU_table.columns))], index=['species'], columns=OTU_table.columns)
        for species in Speciesall:
            Newrow = pd.DataFrame([[0] * (len(OTU_table.columns))], index=[species], columns=OTU_table.columns)
            Sprowbpb = Sprowbpb.append(Newrow)
        # set up commensal butyrate producing species matrix
        Sprowbpbcom = pd.DataFrame([[0] * (len(OTU_table.columns))], index=['species'], columns=OTU_table.columns)
        for species in Speciesall:
            Newrow = pd.DataFrame([[0] * (len(OTU_table.columns))], index=[species], columns=OTU_table.columns)
            Sprowbpbcom = Sprowbpbcom.append(Newrow)
        # abundance times butyrate producing score
        for OTUs in OTU_table_pathogen.index:
            try:
                # calculate species abundance
                # calculate bpb species abundance
                for species in Species[OTUs]:
                    Sprow.loc[species] = Sprow.loc[species] + OTU_table.loc[OTUs]
                    Sprowbpb.loc[species] = Sprowbpb.loc[species] + OTU_table_pathogen.loc[OTUs] * \
                                               OTUwithTraits[OTUs] * OTUwithPathogenTraits[OTUs]
                    Sprowbpbcom.loc[species] = Sprowbpbcom.loc[species] + OTU_table_commensal.loc[OTUs] * \
                                               OTUwithTraits[OTUs] * (1 - OTUwithPathogenTraits[OTUs])
            except KeyError:
                pass
            try:
                OTU_table_pathogen.loc[OTUs] = OTU_table_pathogen.loc[OTUs] * \
                                               OTUwithTraits[OTUs] * OTUwithPathogenTraits[OTUs]
                OTU_table_commensal.loc[OTUs] = OTU_table_commensal.loc[OTUs] * \
                                               OTUwithTraits[OTUs] * (1 - OTUwithPathogenTraits[OTUs])
            except KeyError:
                # OTUs with low abundance that are filtered out
                OTU_table_pathogen.loc[OTUs] = OTU_table_pathogen.loc[OTUs] * 0.0
                OTU_table_commensal.loc[OTUs] = OTU_table_commensal.loc[OTUs] * 0.0
        # calculate total abundance of butyrate producing OTUs
        for OTUs in OTU_table_pathogen.index:
            try:
                if OTUs != 'Abu_with_Traits':
                    OTU_table_pathogen.loc['Abu_with_Traits'] += OTU_table_pathogen.loc[OTUs]
                    OTU_table_commensal.loc['Abu_with_Traits'] += OTU_table_commensal.loc[OTUs]
            except KeyError:
                pass
        Newrow = OTU_table_pathogen.loc['Abu_with_Traits']
        OTU_table_pathogen[0:-1].to_csv(os.path.join(args.r, treefile + '.infertraits.pathogen.otu_table'),
                               sep='\t', header=True)
        Newrow.to_csv(os.path.join(args.r, treefile + '.infertraits.pathogen.abu'), sep='\t',
                      header=True)
        Newrow = OTU_table_commensal.loc['Abu_with_Traits']
        OTU_table_commensal[0:-1].to_csv(os.path.join(args.r, treefile + '.infertraits.commensal.otu_table'),
                               sep='\t', header=True)
        Newrow.to_csv(os.path.join(args.r, treefile + '.infertraits.commensal.abu'), sep='\t',
                      header=True)
        Sprow.to_csv(os.path.join(args.r, treefile + '.species.abu'), sep='\t',
                     header=True)
        Sprowbpb.to_csv(os.path.join(args.r, treefile + '.bpbspecies.pathogen.abu'), sep='\t',
                        header=True)
        Sprowbpbcom.to_csv(os.path.join(args.r, treefile + '.bpbspecies.commensal.abu'), sep='\t',
                        header=True)


################################################### Programme #######################################################
rootofus, treefile = os.path.split(args.t)
traitdir, traitfile = os.path.split(args.rd)
os.system('python '+args.b+' -t ' + str(args.t) + ' -n ' + \
           str(args.n)+' -rd ' + \
           str(args.rd) +' -r ' \
           + str(args.r) )
os.system(('python '+args.b+' -t ' + str(args.t) + ' -n ' + \
           str(args.n)+' -rd ' + \
           str(args.s) +' -r ' \
           + str(args.r)).replace('inferTraits.py','inferTraits_species.py'))
if args.p != 'FALSE':
    os.system('python ' + args.b + ' -t ' + str(args.t) + ' -n ' + \
              str(args.n) + ' -rd ' + \
              str(args.p) + ' -r ' \
              + str(args.r) + ' -tag .pathogen')
    Traitspredicting(os.path.join(args.r, treefile + '.infertraits.txt'),
                     os.path.join(args.r, treefile + '.infertraits.pathogen.txt'),
                     os.path.join(args.r, treefile + '.infertraits.species.txt'))
else:
    Traitspredicting(os.path.join(args.r, treefile + '.infertraits.txt'),
                     args.p,
                     os.path.join(args.r, treefile + '.infertraits.species.txt'))
