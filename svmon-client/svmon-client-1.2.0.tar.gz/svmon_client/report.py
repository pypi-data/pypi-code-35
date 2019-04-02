#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import json
import subprocess
from . import services
from . import json_operations

class SVMONReport:

    def __init__(self):
        self.site=""
        self.host=""
        self.service_names=[]
        self.service_type=""
        self.operating_system=""  
        self.tags=[]
        cwd = os.path.dirname(services.__file__)
        filename = cwd + "/config.json"
        with open(filename, 'r') as f:
            load_dict= json.load(f)
            #print(type(load_dict))
           # for k,v in load_dict.items():
        #    print("%s : %s " %(k,v))
            self.site=str(load_dict['site'])
            self.host=str(load_dict['host'])
            self.service_type=str(load_dict['service_type'])
            #print(type(self.service_type))
            #print(self.service_type)
            #print("mark")
            #if services.in_service_list(self.service_type) == False:
            #    print("service type not configured")
            #self.service_names=services.get_service_name(self.service_type)
           # print(self.service_names)
            #self.tags=services.get_service_tag(self.service_type)
           # print(self.tags)
            #print(self.service_names)
            #print(self.tags)
            

    def refresh_service_name_and_tag(self):
        if services.in_service_list(self.service_type) == False:
            print("service type not configured")
        self.service_names = services.get_service_name(self.service_type)
        self.tags = services.get_service_tag(self.service_type)

    
    def get_site(self):
        return self.site

    def get_host(self):
        return self.host

    def get_service_names(self):
        return self.service_names

    def get_service_type(self):
        return self.service_type

    def get_tags(self):
        return self.tags
    
    def set_site(self,site):
        if isinstance(site,str):
            self.site=site

    def set_host(self,host):
        if isinstance(host,str):
            self.host=host

    def set_service_names(self,service_names):
        if isinstance(service_names,list):
            self.service_names=service_names

    def set_service_type(self,service_type):
        if isinstance(service_type,str):
            self.service_type=service_type

    def set_tags(self,tags):
        if isinstance(tags,list):
            self.tags=tags
   
    def set_operating_system(self,operating_system):
        if isinstance(operating_system,str):
            self.operating_system=operating_system

    def set_service_names_and_tags(self,service_name,tag):
        this.service_names.append(service_name)
        this.tags.append(tag)
       

    def print_report(self):
        if len(self.service_names) > 0:
            res=[]
            if self.service_names== None or len(self.service_names ) < 1:
                print("no service names is resolved at your host")
                exit(1)
            if  self.tags == None or len(self.tags) < 1:
                print("no service component version is resolved at your host")
                exit(1)
            for i in range(len(self.service_names)):
                res.append(self.site+'\t'+self.host+'\t'+self.operating_system+'\t'+self.service_type+'\t'+self.service_names[i]+'\t'+self.tags[i]+'\n')
           # print len(self.service_names)
            #print "here"
            return res
        else:
            print( len(self.service_names))
            #print "there"
            return []



    def jsonify(self):
        if len(self.service_names) > 0:
            res = {}
            res['site']= self.site
            res['host'] = self.host
            res['operating_system'] = self.operating_system
            res['service_type'] = self.service_type
            res['service_names'] = self.service_names
            res['tags'] = self.tags
            return res
        else:
            print("No services to be jsonified")
            return {}
    
    def save_to_json(self):
        if self.site != "" and self.site != None:
            res = {}
            res['site']= self.site
            res['host'] = self.host
            res['service_type'] = self.service_type
            cwd = os.path.dirname(services.__file__)
            #print(cwd)
            #print(type(cwd))
            filename = cwd + "/config.json"
            if services.get_user() != 'root' and cwd.find('usr') != -1 and cwd.find('lib') != -1:
                print('You need root priviledges to write the configuration file')
                exit(1)

            success = json_operations.save_to_file(filename,res)
            if success == False:
                print("Save json data failed")
                exit(1)
        else:
            print("No services to be jsonified")
            exit(1)
    
        
    
 

    def set_pair(self,key,value):
        if isinstance(key,str) == False:
            print("Key should be a string")
            exit(1)

        if key == "site":
            self.set_site(value)
        elif key == "host":
            self.set_host(value)
        elif key == "service_type":
            self.set_service_type(value)
        elif key == "operating_system":
            self.set_operating_system(value)
        elif key == "service_names":
            self.set_service_names(value)
        elif key == "tags":
            self.set_tags(value)
        else :
            print("such key is not supporteed: %s\n" %key)
            exit(1)


    def check_site(self):
        return True


    def check_host(self):
        return True

    def print_config_file(self):
        cwd = os.path.dirname(services.__file__)
        filename = cwd + "/config.json"
        with open(filename, 'r') as f:
            load_dict = json.load(f)
            print("The following are your current configurations: ")
            print('site=  ' +str(load_dict['site']))
            print('host=  ' +str(load_dict['host']))
            print('service type =  ' +str(load_dict['service_type']))
            print('Please use svmon --site <SITE> --host <HOST> --type <TYPE> --dump to change your configuration')



    def send_report_to_svmon_server(self):
       import requests as re
       url = 'https://svmon.eudat.eu:8443/api/serviceComponent/jsonreport'
       headers = {}
       headers['Content-Type'] = 'application/json'
       cwd = os.path.dirname(services.__file__)
       certs = cwd + "/chain_TERENA_SSL_CA_3.pem"
       for i in range(len(self.service_names)):
           res = {}
           res['siteName']=self.site
           res['hostNameId']=self.host
           res['operatingSystem']=self.operating_system
           res['serviceType']=self.service_type
           res['serviceComponentName']=self.service_names[i]
           res['tagAtSite']=self.tags[i]
           r = re.post(url, headers=headers, data=json.dumps(res), verify=certs)
           if (r.status_code != 201):
               print('Sending report failed, please check your configuration')
               exit(1)
       print('Report has been sent successfully.')
       exit(0)



if __name__=="__main__":
    re=SVMONReport()
    re.save_to_json()
