#!/usr/bin/env python
#-*-coding: utf-8 -*-

import os
import sys
import urllib2
from pyhdfs import HdfsClient
try:
    import jaguar_v2
    jaguar_v2.sys_append_paths()
except:
    pass
import json
from base.log import logger

class Client:
    def __init__(self, hosts, user_name):
        self.hosts = hosts
        self.user_name = user_name
        self.client = HdfsClient(hosts, user_name)
    def getClient(self):
        return self.client
    def getHost(self):
        return self.hosts.split(':')[0]
#client = Client().getClient()
def exists(hdfs_path, client):
    return client.exists(hdfs_path)

def delete(hdfs_path, client):
    res = False
    if client.exists(hdfs_path):
        res = client.delete(hdfs_path, recursive = True)
    else:
        return True
    return res

def download(hdfs_path, local_path, client):
    file_name = hdfs_path.split('/')[-1]
    local_path = '%s/%s'%(local_path, file_name)
    if client.exists(hdfs_path):
        try:
            client.copy_to_local(hdfs_path, local_path)
        except Exception, e:
            import traceback
            error_msg = traceback.format_exc()
            logger().error('download faill error:%s'%(error_msg))
            return False  
        return True
    else:
        return False

def download_for_auto(hdfs_path, local_path, client):
    file_name = hdfs_path.split('/')[-1] + '_test'
    local_path = '%s/%s'%(local_path, file_name)
    if client.exists(hdfs_path):
        try:
            client.copy_to_local(hdfs_path, local_path)
        except Exception, e:
            import traceback
            error_msg = traceback.format_exc()
            logger().error('download faill error:%s'%(error_msg))
            return False  
        return True
    else:
        return False

def download_sign(hdfs_path, local_path, sign, client):
    file_name = hdfs_path.split('/')[-1] + '_%s' % sign
    local_path = '%s/%s'%(local_path, file_name)
    if client.exists(hdfs_path):
        try:
            client.copy_to_local(hdfs_path, local_path)
        except Exception, e:
            import traceback
            error_msg = traceback.format_exc()
            logger().error('download faill error:%s'%(error_msg))
            return False  
        return True
    else:
        return False

def download_dir(hdfs_path, local_path, client):
    if hdfs_path[-1] == os.sep:
        hdfs_path = hdfs_path[:-1]
    if local_path[-1] == os.sep:
        local_path = local_path + os.sep
    local_path = local_path + hdfs_path.split(os.sep)[-1]
    hadoop_home = '/opt/hadoop-3.1.0/bin'
    cmd = 'hadoop fs -get %s %s'%(hdfs_path, local_path)
    res = os.system(cmd) == 0
    return res


def upload(local_path, hdfs_path, client):
    file_name = local_path.split('/')[-1]
    hdfs_path = '%s/%s'%(hdfs_path, file_name)
    logger().info('local_path:%s, hdfs_path:%s'%(local_path, hdfs_path))
    res = False
    if delete(hdfs_path):
        try:
            client.copy_from_local(local_path, hdfs_path)
        except Exception, e:
            import traceback
            error_msg = traceback.format_exc()
            logger().error('upload faill error:%s'%(error_msg))
            return False
        res = True
    return res

def listdir(hdfs_path, client):
    return client.listdir(hdfs_path)

def upload_dir(local_path, hdfs_path, client):
    hadoop_home = '/opt/hadoop-3.1.0/bin'
    cmd = '%s/hadoop fs -put -f %s %s'%(hadoop_home, local_path, hdfs_path)
    res = os.system(cmd) == 0
    return res
def get_job_id(job_name, fclient):
    host = fclient.getHost()
    def filter_app(x):
        target_name = x['name']
        return target_name == job_name
    apps_url = 'http://%s:8088/ws/v1/cluster/apps' %host
    print apps_url
    response = urllib2.urlopen(apps_url)
    print apps_url
    data = response.read()
    #print data
    data = json.loads(data)
    apps = data['apps']['app']
    target_apps = filter(filter_app, apps)
    if not target_apps:
        return None
    target_apps = sorted(target_apps, key=lambda x:x['startedTime'], reverse=True)
    target_app = target_apps[0]
    job_id = 'job' + target_app['id'][11:]
    return job_id

if __name__ == '__main__':
    #print 'ds'
    client = Client('192.168.8.31:50070', 'hadoop')
    #print client.getHost()
    print get_job_id('', client)
    #print exists('/production/jaguar/200000143/auto/output/26_20180623055523928.tx')    
    #print upload_dir('./base','/tmp')
    #print delete('/tmp/t.txt')
    #client.copy_from_local('/tmp/t.txt', '/tmp/t.txt')
    #print download('/tmp/t.txt','./')
    #print listdir('/production/jaguar/jaguar/version1/auto/input')
    #print download_dir('/tmp/output/protocol','./')

