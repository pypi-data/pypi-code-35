#!/usr/bin/env python3
#-*- coding: utf-8 -*- 

import sys,os
import time,random

from sys import exit
from random import randint 
from time import strftime
from time import sleep

"""
Validator : filter + validator
"""
class Validator:
    def __init__(self):
        self._errors=[]
        self._data={}
        self._failed=False
        self._attrs={}
        self._allow_keys=[]
        self._default_data={}
        self._filters={}
        self._messages={
                'required':'%s 字段未提供',
                'min':'%s 不能小于 %s',
                'max':'%s 不能大于 %s',
                }

    def setFilter(self,name,options={}):
        self._filters[name]=options

    def setDefaultData(self,data):
        self._default_data=[]

    def setAllowKeys(self,keys=[]):
        self._allow_keys=keys
                
    def setMessage(self,rule,format_string):
        self._messages[rule]=format_string

    def setAttr(self,name,label):
        self._attrs[name]=label

    def addError(self,name,rule,message=''):
        self.failed= True
        self._errors.append(self.getMessage(rule,name,message))

    def getErrors(self):
        return self._errors

    def getError(self):
        if self._errors:
            return self._errors[0]
        else:
            raise BaseException("No Error Happend")

    def fails(self):
        return self._failed

    def getData(self):
        return self._data;

    def getMessage(self,rule,name,value):
        name=self.getAttr(name)
        if rule == 'required':
            message = self._messages[rule] %(name)
        else:
            message = self._messages[rule] %(name,value)

        return message


    def getAttr(self,name):
        if name in self._attrs:
            return self._attrs[name]
        else:
            return name


    def filter(self,data):
        for name,filter in self._filters.items():
            filters=filter.split('|')
            for filter in filters:
                if filter == 'trim' and name in data:
                    data[name] = data[name].strpi()
                elif filter == 'toint' and name in data:
                    data[name] = int(data[name])
                elif filter == 'tostring' and name in data:
                    data[name] = str(data[name])

        return data


    def valid(self,data,rules):
        """
            use allow keys to filter
            use filter to filter
            use rules to check
        """

        filter_data=self._default_data;
        for key in self._allow_keys :
            if key in data and data[key] != None:
                filter_data[key]=data[key]

        filter_data=self.filter(filter_data)


        for name,value  in rules.items():
            cols=value.split('|')
            for col in cols:
                if col.find(":") == -1: col+=":_|"
                v=col.split(":")

                #required
                if not name in filter_data  or not filter_data[name] :
                    self.addError(name,'required')
                    return False

                if v[0] == 'required':
                    pass
                elif v[0] == 'min':
                    if int(data[name]) < int(v[1]):
                        self.addError(name,'min',v[1])
                        return False
                elif v[0] == 'max':
                    if int(data[name]) > int(v[1]):
                        self.addError(name,'max',v[1])
                        return False

        
        self._data=filter_data

        return True

                    








if __name__ == '__main__':
    v=Validator();

    data={
            'name':'frd',
            'age':13,
            'id':'3',
            }

    rules={
            'id':'required',
            'age':'min:12',
            }


    v.setAllowKeys(['id','name','age'])
    v.setFilter('id','toint')
    ret=v.valid(data,rules)

    if ret :
        print(v.getData())
    else:
        print(v.getErrors())


