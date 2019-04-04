#!/usr/bin/env python3
# -*- coding: utf-8 -*- 

import json
import httplib2
from xml.dom.minidom import parse
import xml.dom.minidom

from ldap3 import Server, Connection, ALL, SUBTREE, ServerPool
#author: guojial@cn.ibm.com
#version: v1.11
#Date:   2019-04-03
#Last Modified by: guojial@cn.ibm.com
#Last Modified time: 2019-04-04

class ibmBluepages:
    
    #from Bluepages get person's information.
    def getPersonInfoByIntranetID(self, intranetID):
        
        http = httplib2.Http() 
        content = http.request("https://bluepages.ibm.com/BpHttpApisv3/slaphapi?ibmperson/mail="+intranetID+".list/byxml", "GET")
        #print(content)
        
        DOMTree = xml.dom.minidom.parseString(content[1])
        collection = DOMTree.documentElement
        
        attrs = collection.getElementsByTagName("attr")
        
        attrData = {}
        for attr in attrs:
            #print (attr.getAttribute('name') + "  :  " + attr.getElementsByTagName('value')[0].childNodes[0].data)
            attrData[attr.getAttribute('name')] = attr.getElementsByTagName('value')[0].childNodes[0].data
        
        #print(attrData)
        personInfo = json.dumps(attrData)
        #print(personInfo)
        return personInfo

    #authenticate the person existed in Bluepages
    def authenticate(self, username, password):

        LDAP_SERVER_POOL = "ldaps://bluepages.ibm.com"
        LDAP_SERVER_PORT = 636
        SEARCH_BASE = "ou=bluepages,o=ibm.com"

        ldap_server_pool = ServerPool(LDAP_SERVER_POOL) 
        conn = Connection(ldap_server_pool, check_names=True, lazy=False, raise_exceptions=False) 
        #print(conn)
        conn.open()
        conn.bind()
        #print(conn)
        
        personInfo = self.getPersonInfoByIntranetID(username)
        personInfo = eval(personInfo)
        #print(personInfo["uid"])

        res = conn.search(search_base = SEARCH_BASE, search_filter = '(uid='+ personInfo["uid"] +')', search_scope = SUBTREE)
        #print(res)

        if res:
            entry = conn.response[0]
            #print(entry)
            dn = entry['dn'] 
            attr_dict = entry['attributes'] 

            # check password by dn
            try: 
                conn2 = Connection(ldap_server_pool, user=dn, password=password, check_names=True, lazy=False, raise_exceptions=False) 
                conn2.bind() 
                #print(conn2.result)
                
                if conn2.result["description"] == "success":
                    #print("success")
                    return True
                else: 
                    #print("auth fail")
                    return False 
            except Exception as e:
                #print("auth fail")
                return False
        else:
            return False