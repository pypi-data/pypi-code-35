#!/Users/ericalm/anaconda/envs/py36/bin/python
import argparse
import os
import random
import math
import csv
import re
import sys
import pandas as pd
import numpy as np
from Bio import SeqIO
from Bio.Blast.Applications import NcbiblastnCommandline
from Bio import SearchIO
from Bio import Phylo
from functools import reduce


############################################ Arguments and declarations ##############################################
parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("-t",
                    help="file name of your tree", type=str, default='16S.nwk',metavar='16S.nwk')
parser.add_argument("-n",
                    help="file name of your tree node names", type=str, default='16S.format.name',metavar='16S.format.name')
parser.add_argument("-rd",
                    help="the reference data of gene traits", type=str, default='Data.txt',metavar='Data.txt')
parser.add_argument("-r",
                    help="results_dir", type=str, default='Bayers_model',metavar='Bayers_model')


################################################## Definition ########################################################
args = parser.parse_args()
try:
    os.mkdir(args.r)
except OSError:
    pass


################################################### Function ########################################################
def read_table(filename,reverse=0):
    table = {}
    f = open(filename,'r')
    lines = [ x.rstrip("\n").split() for x in f ]
    if reverse:
        lines = [ (v,k) for (k,v) in lines ]
    for k,v in lines:
        table[k] = v
    f.close()
    return table

def assign_internal_names(tree):
    names = {}
    for idx, clade in enumerate(tree.find_clades()):
        if clade.name:
            old_name = clade.name
            clade.name = '%d_%s' % (idx, clade.name)
        else:
            old_name = None
            clade.name = str(idx)
        if old_name:
            names[old_name] = clade.name
    return names

def mismatch(c,chars):
    return len([x for x in chars if c not in x])

def pars(chars):
    # clade terminal
    if not chars:
        return set()
    # internal clades
    # chars is all scores of clades under the internal clades
    # all_chars is all unique stored anno/scores in chars
    all_chars = set(reduce( lambda a,b: a.union(b), chars ))
    # scores are [a score, number of different scores]
    scores = [(c,mismatch(c,chars)) for c in all_chars]
    # min_score is the minimum number of different scores
    min_score = min(scores,key=lambda x:x[1])[1]
    # choose the scores of highest agreement (minimum number of different scores)
    # we set 0.5 as the cutoff
    # return {0.0} for more 0.0 than 1.0
    # return {1.0} for more 1.0 than 0.0
    # return {0.0, 1.0} for half 0.0 and half 1.0 (final result is 0.5)
    return set([x[0] for x in scores if not x[1] > min_score])

def down_pass(clade,data,anno):
    # set the anno/scores from bottom to up
    for x in clade.clades:
        down_pass(x,data,anno)
    # set anno to reference terminal clades
    if clade.name in anno:
        data[clade.name] = set(anno[clade.name])
        return
    # ignore unknown terminal clades
    if clade.is_terminal():
        return
    # infer traits for internal clades that have reference terminal clades below
    # based on all scores of clades under the internal clades
    # pass the scores of highest agreement (minimum number of different scores)
    chars = pars([ data[x.name] for x in clade.clades if x.name in data ])
    if chars:
        data[clade.name] = chars
    return

def up_pass(parent_chars,clade,data,anno):
    # set the anno/scores from up to bottom
    # reference terminal clades
    if clade.name in anno:
        data[clade.name] = set(anno[clade.name])
        if clade.is_terminal():
            return
    else:
        # correct scores for internal clades using parent scores
        # based on the scores of parent and itself
        if clade.name in data:
            data[clade.name] = pars([data[clade.name],parent_chars])
        # infer traits for internal clades that have no reference terminal clade below
        # infer traits for unknown terminal clades
        # pass the scores of parent
        else:
            data[clade.name] = parent_chars
    for x in clade.clades:
        up_pass(data[clade.name],x,data,anno)
    return


################################################### Programme #######################################################
workingDir, filename = os.path.split(args.t)
treefile = args.t
nodenamefile = args.n
annotationfile = args.rd

# read annotation files of traits in references (0.0 or 1.0)
anno = read_table(annotationfile)
# get numericIDs for each name
nodename = read_table(nodenamefile,1)

tree = Phylo.read(treefile, 'newick')
# assign names to internal nodes
internal_names = assign_internal_names(tree)
# switch annotations to new names
anno = dict([ (internal_names[nodename[k]],v) for (k,v) in anno.items() ])

# data stores the scores of internal and terminal clades
data = {}
# set the scores of internal and reference terminal clades
down_pass(tree.clade,data,anno)
up_pass(set(),tree.clade,data,anno)

leaves = [ (x,data[x]) for x in data.keys() if '_' in x ]
old_names = dict([ (v,k) for (k,v) in nodename.items() ]) #123->abc.fasta
new_names = dict([ (v,k) for (k,v) in internal_names.items() ]) #789_123->123

missing = []
f1=open(os.path.join(args.r,filename+'.infertraits.txt'),'w')
# output the mean score of the scores with the highest agreement (0.0, 0.5 or 1.0)
for k,v in leaves:
    if new_names[k] in old_names and k not in anno:
        print ([v,np.mean(list(map(int, list(v))))])
        f1.write(old_names[new_names[k]]+'\t'+str(np.mean(list(map(int, list(v)))))+'\n')
    else:
        missing += [new_names[k]]
f1.close()
#print('Warning missing nodes in tree: ', missing)
