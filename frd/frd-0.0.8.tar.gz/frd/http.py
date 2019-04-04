#!/usr/bin/env python3
#-*- coding:utf-8 -*-

"""
 http module
"""

import requests
import pprint

class Http:
    def __init__(self,baseurl=""):
        self.baseurl=baseurl
        self.request=requests.Session()

        self.options={
            'response_data_type':'json',
            'exception_handler':self.handleException,
        }

        self.logger=None
        self.log_enable=False

    def setLogger(self,logger):
        self.logger=logger
        self.enableLogger()

    def enableLogger(self):
        self.log_enable=True

    def disableLogger(self):
        self.log_enable=True

    def handleException(self,r):
        print(r.status_code)
        print(r.text)
        exit()#

    def setOption(self,k,v):
        self.options[k]=v

    def getOption(self,k):
        if k in self.options:
            return self.options[k]
        else:
            return null

    def get_url(self,path):
        return self.baseurl+path

    def get(self,path,params={}):
        url=self.get_url(path)

        if self.log_enable :
            self.logger.info("GET: "+url)
            self.logger.info("GET Params: "+pprint.pformat(params))

        r=self.request.get(url,params=params)

        if self.log_enable :
            self.logger.info("Response Status Code: "+str(r.status_code))
            self.logger.info("Response Content ")
            self.logger.info(r.text)

        if r.status_code != 200:
            self.handleException(r)
            return False

        if self.options['response_data_type'] == "text":

            return r.text
        else:
            try:
                content= r.json()

                return content

            except ValueError:
                self.handleException(r)
                return False

    def post(self,path,params={},files=None,json=None):
        url=self.get_url(path)

        if self.log_enable :
            self.logger.info("POST: "+url)
            self.logger.info("Post Params: "+pprint.pformat(params))

        r=self.request.post(url,data=params,files=files,json=json)


        if self.log_enable :
            self.logger.info("Response Status Code: "+str(r.status_code))
            self.logger.info("Response Content ")
            self.logger.info(r.text)

        if r.status_code != 200:
            self.handleException(r)
            return False

        if self.options['response_data_type'] == "text":
            return r.text
        else:
            try:
                return r.json()
            except ValueError:
                self.handleException(r)
                return False

    def close(self):
        self.request.close();




"""
    http=Http()
    http.setOption('exception_handler',exception_hander)
    http.get(url,params
    http.post(url,params)

    if exception:
        will show message and exit
"""

