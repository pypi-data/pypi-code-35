#!usr/bin/env python
#encoding:utf-8
from __future__ import division

'''
__Author__:沂水寒城
功能： 博客文章下载器
'''


import re 
import os
import sys
import json
import time
import random
import requests
import urllib
import urllib2
from urllib import urlopen
from bs4 import BeautifulSoup
from urllib import urlretrieve
from lxml import etree,html
from fake_useragent import UserAgent

import sys
reload(sys)
sys.setdefaultencoding( "utf8" )



def generate_random_UA(num=100):
    '''
    生成随机的 User-Agent 字符串（使用第三方海量ua库）
    '''
    agent_list=[]
    user_agent=UserAgent()
    for i in range(num):
        one_agent=user_agent.random
        agent_list.append(one_agent)
    return agent_list


def callback(dbnum, dbsize, size):
    '''
    回调函数
    dbnum: 已经下载的数据块
    dbsize: 数据块的大小
    size: 远程文件的大小
    '''
    percent=100.0*dbnum*dbsize/size
    if percent>100:
        percent=100
    print "%.2f%%"% percent


def getCsdnUrls(url,blog_name):
    '''
    获取 CSDN 中的文章链接
    '''
    res_list=[]
    header_list=generate_random_UA(num=200)
    # ip_list=json.load(open('valid_ip_all.json'))  #valid_ip333
    # print 'ip_list_length: ',len(ip_list)
    headers={'User-Agent':random.choice(header_list)}
    request=urllib2.Request(url, headers=headers)
    response=urllib2.urlopen(request)
    contents=response.read()
    soup=BeautifulSoup(contents, "html.parser")
    for h4 in soup("h4"):
        url=h4("a")[0]["href"]
        print 'url: ',url
        if url.find(blog_name)!=-1:
            res_list.append(url)
    return res_list


def downloadPapers(res_list,saveDir='blogPapers/'):
    '''
    下载文章数据
    '''
    if not os.path.exists(saveDir):
        os.makedirs(saveDir)
    for one_url in res_list:
        local_path=saveDir+one_url.split('/')[-1].strip()+'.html'
        urllib.urlretrieve(one_url,local_path,callback)


def blogSpiders(blog_name='blog_name',num=10,saveDir='blogPapers/'):
    '''
    博客数据爬虫
    '''
    for i in range(1,num):
        one_res=getCsdnUrls("https://blog.csdn.net/"+str(blog_name)+"/article/list/%d" % i,blog_name)
        downloadPapers(one_res,saveDir=saveDir+str(i)+'/')


if __name__ == '__main__':
    print 'blogDownloader!!!'
    # para_list=sys.argv
    # blog_name=para_list[1]
    # for i in range(1,36):
    #     one_res=getCsdnUrls("https://blog.csdn.net/"+str(blog_name)+"/article/list/%d" % i,blog_name)
    #     downloadPapers(one_res,saveDir='blogPapers/'+str(i)+'/')
    # 
 
 
