#!/usr/bin/env python3
#-*- coding: utf-8 -*- 
"""
Simple Json DB

save json data to a file ,and read it 

"""

import sys,os
import time,random

from sys import exit
from random import randint 
from time import strftime
from time import sleep

import hashlib,shutil,time
import glob
import requests
import json


class JsonDb:
    def __init__(self,path):
        self.data={}

        self.path=path
        self.connect()

    def connect(self):
        if os.path.exists(self.path):
            fp=open(self.path,"r",encoding="utf-8")
            self.data=json.load(fp)

            return True

        return False

    def get(self,name,default=None):
        if name in self.data:
            return self.data[name]
        else:
            return default

    def set(self,name,value):
        self.data[name]=value

    def remove(self,name):
        del self.data[name]

    def exists(self,name):
        return name in self.data

    def save(self):
        fp=open(self.path,"w")
        json.dump(self.data,fp,indent=2)
        fp.close()

        return True

