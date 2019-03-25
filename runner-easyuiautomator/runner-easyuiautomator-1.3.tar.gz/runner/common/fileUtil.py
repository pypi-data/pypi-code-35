# coding=utf-8
'''
Created on 2017年3月22日

@author: fengbo
'''

class FileUtil(object):
    '''
    Add File
    '''
    @staticmethod
    def writeData(filename,data):
        with open(filename + ".txt", "a") as f:
            f.write(data+'\n')
        