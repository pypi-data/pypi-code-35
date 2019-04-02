#! /Users/xiaotian/anaconda3/bin/python3.6
#coding=utf-8

import os.path
from ComplexTDL.CurrentPath import *

def ShowJobModules():

    with open(BASEPATH + 'WorkType.txt', 'r') as f:
        print(f.read())
    
    rp = os.path.realpath(__file__)
    fp = os.path.split(rp)[0]

    print('You can change the settings in the file "WorkType" under ' + fp)


def ShowDefaultJobModule():

    print('''importantJobs = [] # the jobs will appear in the top of the report
smallJobs = [] # the jobs which will not appear in the project report
myJobs = [] # the jobs which will not appear in the work report''')


def SetTaskNumber(number):

    try:

        n = int(number)
        with open(BASEPATH + 'number.txt', 'w') as f:
            f.write(number)
        
        print('Settings modified')
    
    except:

        print('Parameters error')