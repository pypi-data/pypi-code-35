#!/usr/bin/env python3
#-*- coding: utf-8 -*- 
"""
ES
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


class Es:
    def __init__(self,index,host="127.0.0.1",port=80):
        self._index=index
        #一个index只能有一个doc_type,所以设置他们为一致，比较方便且简单
        self._doc_type=index 

        #self.es= Elasticsearch()
        self.es= Elasticsearch([{'host':host,'port':port}])

    
    #每次默认返回10个， 怎么办?
    def searchAll(self):
        res = self.es.search(index=self._index,doc_type=self._doc_type,body={"query":{"match_all":{}}})

        return res

    def getList(self,page,page_count=10):
        i=0 
        body={
          'size':page_count,
          'from':(page-1)*page_count,
          'query' :{
          'match' :{
               #'category':'book',

              },
           },
          "sort":[
          {
            "star" :{ "order" : "asc"}
          }
          ]
        }


        res = self.es.search(index=self._index,doc_type=self._doc_type,body=body)

        return res

    def total(self):
        res=self.searchAll()

        return res['hits']['total']
    
    def get(self,item_id):
        res = self.es.get(index=self._index, doc_type=self._doc_type, id=item_id)

        return res

    def search(self,keyname,value):
        res = self.es.search(index=self._index, doc_type=self._doc_type,
                             body={"query":{"match":{keyname:value}}})
        return res

    def deleteAll(self):
        i=0

        res=self.searchAll()
        for item in res['hits']['hits']:
            print(item['_id'])
            self.es.delete(index=self._index,doc_type=self._doc_type,id=item['_id']);

            i+=1

        return i

    def delete(self,item_id):
        self.es.delete(index=self._index,doc_type=self._doc_type,id=item_id)

    def defineIndex(self,mapping):
        """
        index_mapping={
            'mappings':{
                'test':{
                    "properties":{
                        "category":{
                            "type":"keyword",
                        },
                        "title":{
                            "type":"text",
                        },
                        "content":{
                            "type":"text",
                        },
                    },
                },
            }
        }
        """

        return self.indices.create(index=self._index,body=mapping)

    def index(self,item):

        if "id" in item:
            item_id=item['id'];
            del item['id']
        else:
            item_id=None
        
        return self.es.index(index=self._index,doc_type=self._doc_type,id=item_id,body=item)

