#!/usr/bin/python
'''
########################################################
#####                                                  #
#####                  catmatch                        #
#####                  R.THOMAS                        #
#####                    2018                          #
#####                    Main                          #
#####                                                  #
##### Usage:  catmatch  [-h] cat1 cat2 column_name #####
#####--------------------------------------------------#
#####                                                  #
########################################################
@License: GPL - see LICENCE.txt
'''

####Public General Libraries
import warnings
import os
import sys

####third party
from tqdm import tqdm
from catscii import catscii
import  numpy

####local imports
from . import cli

class missing_in_header(Exception):
    def __init__(self, value):
        self.error = value

def custom_formatwarning(matchline, *args, **kwargs):
    line = '\033[93m'+'There is more than one or no entry for %s in the second catalog, '%matchline
    line += 'please check because We skip this line'+'\033[0m'
    return line + '\n'

warnings.formatwarning = custom_formatwarning

def check_final_header(header1, header2, column):
    '''
    This function checks the header
    and produce the final header
    Parameters:
    -----------
    header1
            list, of all the column names from cat1
    header2
            list, of all the column names from cat2
    column
            str, column that will be matched

    Returns:
    --------
    final_header 
            list, of all the column to be written in the final catalog
    '''

    ###for each column in header2, we check if it is as well in header1
    ###if so, we add '_1' at the end of the column name from header2

    head2 = []
    for i in header2:
        #if i != column:
            if i in header1:
                head2.append(i+'_1')
            else:
                head2.append(i)

    header = ''
    for i in header1+head2:
        header += '%s\t'%i
    
    return header


def readlines():
    '''
    Method that open the catalog and read the lines
    '''
    with open(self.cat, 'r') as F:
        Fl = F.readlines()
   
    self.readlinescat = Fl
    self.header_line = Fl[0][1:-1]


def match(cat1, cat2, column):
    '''
    Function that crossmatch the catalog

    Parameter:
    ----------
    cat1    catscii object, of the first catalog
    cat2    catscii object, of the second catalog
    column  str, name of the column to match

    Return:
    -------
    final_cat       numpy.array 
                    
    final_header 
                    list, of column names for the final file
    '''

    ###create the final header
    final_header = check_final_header(cat1.header, cat2.header, column)

    ###we start matching 
    final_cat = []

    #a-get the column
    col1 = cat1.get_column(column, 'str')
    col2 = cat2.get_column(column, 'str')

    for i in tqdm(range(len(col1))):
        #we look where i is in cat2 (col2)
        index_cat2 = list(numpy.where(col2 == col1[i])[0])
        if len(index_cat2) > 1:
            warnings.warn(col1[i])
        if not index_cat2:
            warnings.warn(col1[i])
        else:
            line1 = list(cat1.get_line(column, col1[i])[0].values())
            line2 = list(cat2.get_line(column, col1[i])[0].values())
            final_line = numpy.array(line1+line2)
            final_cat.append(final_line)
 
    return numpy.array(final_cat), final_header

def main():
    '''
    This function is the main of the catmatch.
    '''
    ###1- we retrive the arguments
    args = cli.CLI().arguments

    ###2-we create the cat objects
    cat1 = catscii.load_cat(args.file1, True)
    cat2 = catscii.load_cat(args.file2, True)

    ###3 -check if the column name is in the two headers
    if args.column in cat1.header and args.column in cat2.header:
        print('\033[1m' + \
                '[INF] Column to match found in both files...we start matching...'+'\033[0m')
    else:
        raise missing_in_header('-- %s -- not found in either or both headers'%args.column)
        
    ###4 - and we start matching
    final_cat, final_header = match(cat1, cat2, args.column) 

    ###5 and save it
    numpy.savetxt(args.outputfile, final_cat, header=final_header, fmt='%s\t')
