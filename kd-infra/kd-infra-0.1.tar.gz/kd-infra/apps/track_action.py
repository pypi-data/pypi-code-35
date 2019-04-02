#!/usr/bin/env python
#-*-coding: utf-8 -*-

import os
import sys
import json
import gzip
import urllib
import urllib2

#import base_conf
import hdfs_util
from singleton import *
from log import logger
import service_config

host_ip = service_config.GET_CONF('hbase','ngnix_ip')

def unzip(gz_file_path, unzip_file_name):
    try:
        logger().info('unzip gz_file_path[%s] to unzip_file_name[%s]' % (
            gz_file_path, unzip_file_name))
        gz_file = gzip.open(gz_file_path, 'rb')
        unzip_file = open(unzip_file_name, 'w')
        unzip_file.write(gz_file.read())
        os.remove(gz_file_path)
        gz_file.close()
        unzip_file.close()
        return True
    except Exception as e:
        err_msg = traceback.format_exc()
        logger().error(err_msg)
        return False

@singleton
class TrackManager():
    def __init__(self):
        self.wirte_batch_url = 'http://%s/track/batch/set'%(host_ip)
        self.get_newest_batch_url = 'http://%s/track/batch/get'%(host_ip)
        self.get_track_path_url = 'http://%s/track/location/get'%(host_ip)
        self.save_track_path_url = 'http://%s/track/location/set'%(host_ip)
        self.save_full_track_path_url = 'http://%s/full_reco/track/location/set'%(host_ip)
        self.get_full_track_path_url = 'http://%s/full_reco/track/location/get'%(host_ip)
        self.element_save_track_path_url = 'http://%s/kv/set/v2' %(host_ip)
        self.element_get_track_path_url = 'http://%s/kv/get/v2' %(host_ip)
        self.element_write_batch_url = 'http://%s/kv/set/v2' %(host_ip)
        self.element_get_newest_batch_url = 'http://%s/kv/get/v2' %(host_ip)

    def wirte_batch_to_hbase(self, trackid, batch):
        formdata = {
            "trackId": trackid,
            "batch": batch
        }
        data = urllib.urlencode(formdata)
        req = urllib2.Request(self.wirte_batch_url, data = data)
        ret = urllib2.urlopen(req)
        result = False
        status = ret.getcode()
        if status == 200:
            res = ret.read()
            logger().info('response is %s ,trackid:%s'%(res, trackid))
            result = json.loads(res)['result']
        else:
            logger().error('write batch to hbase fail trackid:%s, batch:%s' \
                            % (trackid, batch))
            return False
        return result

    def wirte_full_batch_to_hbase(self, trackid, batch):
        formdata = {
            "trackId": trackid + '_full',
            "batch": batch
        }
        data = urllib.urlencode(formdata)
        req = urllib2.Request(self.wirte_batch_url, data = data)
        ret = urllib2.urlopen(req)
        result = False
        status = ret.getcode()
        if status == 200:
            res = ret.read()
            logger().info('write full batch response is %s ,trackid:%s'%(res, trackid))
            result = json.loads(res)['result']
        else:
            logger().error('write full batch to hbase fail trackid:%s, batch:%s' \
                            % (trackid, batch))
            return False
        return result

    def get_newest_batch(self, trackid):
        get_batch_url = "%s?trackId=%s"%(self.get_newest_batch_url, trackid)
        
        ret = urllib2.urlopen(get_batch_url)
        batch = None
        status = ret.getcode()
        if status == 200:
            res = ret.read()
            batch = json.loads(res)['result']
        else:
            logger().error('get newest batch request fail status is %s'%status)
            return None
        return batch

    def get_full_track_newest_batch(self, trackid):
        get_batch_url = "%s?trackId=%s"%(self.get_newest_batch_url, trackid + '_full')
        print get_batch_url
        ret = urllib2.urlopen(get_batch_url)
        batch = None
        status = ret.getcode()
        if status == 200:
            res = ret.read()
            batch = json.loads(res)['result']
        else:
            logger().error('get full track newest batch request fail status is %s'%status)
            return None
        return batch

    def get_track_path(self, trackid, batch):
        url = '%s?trackId=%s:%s'%(self.get_track_path_url, trackid, batch)
        ret = urllib2.urlopen(url)
        track_path = None
        status = ret.getcode()
        if status == 200:
            res = ret.read()
            track_path = json.loads(res)['result']
        else:
            logger().error('get track path fail status:%s, trackid:%s, batch:%s'%(status, trackid, batch))
        return track_path

    def get_full_track_path(self, trackid, batch):
        url = '%s?track_id_batch=%s_full:%s'%(self.get_full_track_path_url, trackid, batch)
        print url
        ret = urllib2.urlopen(url)
        track_path = None
        status = ret.getcode()
        if status == 200:
            res = ret.read()
            track_path = json.loads(res)['result']
        else:
            logger().error('get track path fail status:%s, trackid:%s, batch:%s'%(status, trackid, batch))
        return track_path

    #download track return download result and local file path
    def download_track(self, trackid, local_path):
        batch = self.get_newest_batch(trackid)
        if not batch:
            logger().error('batch is None trackid:%s'%(trackid))
            return [False,None]
        track_path = self.get_track_path(trackid, batch)
        if not track_path:
            logger().error('track_path is None trackid:%s, batch:%s'%(trackid, batch))
            return [False,None]
        file_name = track_path.split('/')[-1]
        file_path = '%s/%s'%(local_path, file_name)
        res = hdfs_util.download(track_path, local_path)
        return [res, file_path]

    def download_track_v2(self, trackid, batch, local_path):
        if not batch:
            logger().error('batch is None trackid:%s'%(trackid))
            return [False,None]
        track_path = self.get_track_path(trackid, batch)
        if not track_path:
            logger().error('track_path is None trackid:%s, batch:%s'%(trackid, batch))
            return [False,None]
        file_name = track_path.split('/')[-1] + '_test'
        print file_name
        file_path = '%s/%s'%(local_path, file_name)
        res = hdfs_util.download_for_auto(track_path, local_path)
        return [res, file_path]

    def download_full_track(self, trackid, local_path):
        batch = self.get_full_track_newest_batch(trackid)
        print batch
        if not batch:
            logger().error('batch is None trackid:%s'%(trackid))
            return [False,None]
        track_path = self.get_full_track_path(trackid, batch)
        logger().info('trackid [%s] batch [%s] hdfs path [%s]', trackid, batch, track_path)
        if not track_path:
            logger().error('track_path is None trackid:%s, batch:%s'%(trackid, batch))
            return [False,None]
        file_name = track_path.split('/')[-1]
        file_path = '%s/%s'%(local_path, file_name)
        res = hdfs_util.download(track_path, local_path)
        return [res, file_path]

    def get_full_track_newest_batch(self, trackid):
        #get_batch_url = "%s?trackId=%s"%(self._url_get, trackid + '_full')
        get_batch_url = "%s?trackId=%s"%(self.get_newest_batch_url, trackid + '_full')
        #print get_batch_url
        ret = urllib2.urlopen(get_batch_url)
        batch = None
        status = ret.getcode()
        if status == 200:
            res = ret.read()
            batch = json.loads(res)['result']
        else:
            logger().error('get full track newest batch request fail status is %s'%status)
            return None
        return batch

    def save_track_path(self, row_key, track_path):
        formdata = {"trackId": row_key, "location": track_path}
        data = urllib.urlencode(formdata)
        req = urllib2.Request(self.save_track_path_url, data = data)
        ret = urllib2.urlopen(req)
        status = ret.getcode()
        if status == 200:
            result = ret.read()
            if json.loads(result)['code'] == '0':
                return True
        return False

    def save_full_track_path(self, row_key, track_path):
        formdata = {"track_id_batch": row_key, "track_file_path": track_path}
        data = urllib.urlencode(formdata)
        req = urllib2.Request(self.save_full_track_path_url, data = data)
        ret = urllib2.urlopen(req)
        status = ret.getcode()
        if status == 200:
            result = ret.read()
            if json.loads(result)['code'] == '0':
                return True
        return False

    def element_write_batch_to_hbase(self, trackid, batch):
        data = batch
        write_batch_url = '%s?key=%s&namespace=%s' %(self.element_write_batch_url,
                        trackid, 'element_classification')
        req = urllib2.Request(write_batch_url, data = data)
        ret = urllib2.urlopen(req)
        status = ret.getcode()
        result = False
        if status == 200:
            res = ret.read()
            logger().info('response is %s, trackid:%s' %(res, trackid))
            result = json.loads(res)['result']
        else:
            logger().error('write batch to hbase fail trackid:%s ,batch:%S'
                            % (trackid, batch))
            return False
        return result

    def element_get_newest_batch(self, trackid):
        get_batch_url = '%s?key=%s&namespace=%s' %(self.element_get_newest_batch_url,
                        trackid,'element_classification')
        ret = urllib2.urlopen(get_batch_url)
        batch = None
        status = ret.getcode()
        if status == 200:
            res = ret.read()
            content_type = ret.headers.getheader('Content-Type')
            if 'application/json' == content_type:
                return None
            batch = res.strip()
        else:
            logger().error('get newest batch request fail status is %s' %status)
            return None
        return batch

    def element_save_track_path(self, rowkey, track_path):
        save_track_path_url = '%s?key=%s&namespace=%s'%(self.element_save_track_path_url
                                                        ,rowkey
                                                        ,'element_classification')
        data = track_path
        req = urllib2.Request(save_track_path_url, data = data)
        ret = urllib2.urlopen(req)
        status = ret.getcode()
        if status == 200:
            result = ret.read()
            if json.loads(result)['code'] == '0':
                return True
        return False

    def element_get_track_path(self, rowkey):
        url = '%s?key=%s&namespace=%s' %(self.element_get_track_path_url
                                        ,rowkey ,'element_classification')
        print url
        ret = urllib2.urlopen(url)
        track_path = None
        status = ret.getcode()
        if status == 200:
            res = ret.read()
            content_type = ret.headers.getheader('Content-Type')
            if 'application/json' == content_type:
                return None
            track_path = res.strip()
        else:
            logger().error('get track path fail status:%s, '
                            'trackid:%s' %(status, trackid))
        return track_path

    def element_get_track_data(self, track_id ,batch ,target_path):
        rowkey = '%s-%s' %(track_id, batch)
        track_manager = TrackManager()
        track_path = track_manager.element_get_track_path(rowkey)
        if not track_path:
            logger().error('element path is null, rowkey[%s]' % rowkey)
            return [False, None]
        file_name = track_path.split('/')[-1]
        if track_path.endswith('.gz'):
            file_name = file_name.split('.gz')[0]
        local_file_path = target_path + os.sep + file_name + '_element'
        track_path
        logger().info('track_file_path:%s' %(track_path))
        if track_path.endswith('.gz'):
            gzip_file_name = track_path.split('/')[-1]
            gzip_file_path = target_path + os.sep + gzip_file_name
            res = hdfs_util.download(track_path, target_path)
            if res:
                res = unzip(gzip_file_path, local_file_path)
        else:
            res = hdfs_util.download_sign(track_path, target_path, 'element')
        if not res:
            logger().error('download %s failure' %(track_path))
            return [False, None]
        else:
            logger().info('download %s success' %(track_path))
            return [True, local_file_path]

    def element_get_full_track_data(self, track_id ,target_path):
        full_newest_batch = get_full_track_newest_batch(track_id)
        if not full_newest_batch:
            logger().info('track_id[%s] no full newest batch' % track_id)
            return [Fasle, None]
        batch = '!!!:%s' % full_newest_batch
        rowkey = '%s-%s' %(track_id, batch)
        track_manager = TrackManager()
        track_path = track_manager.element_get_track_path(rowkey)
        if not track_path:
            logger().error('element full pb path is null, rowkey[%s]' % rowkey)
            return [False, None]
        file_name = track_path.split('/')[-1]
        if track_path.endswith('.gz'):
            file_name = file_name.split('.gz')[0]
        local_file_path = target_path + os.sep + file_name + '_full_element'
        logger().info('track_file_path:%s' %(track_path))
        if track_path.endswith('.gz'):
            gzip_file_name = track_path.split('/')[-1]
            gzip_file_path = target_path + os.sep + gzip_file_name
            res = hdfs_util.download(track_path, target_path)
            if res:
                res = unzip(gzip_file_path, local_file_path)
        else:
            res = hdfs_util.download_sign(track_path, target_path, 'full_element')
        if not res:
            logger().error('download %s failure' %(track_path))
            return [False, None]
        else:
            logger().info('download %s success' %(track_path))
            return [True, local_file_path]

def get_track_data(trackid, local_path):
    track_manager = TrackManager()
    return track_manager.download_track(trackid, local_path)

def get_track_data_v2(trackid, batch, local_path):
    track_manager = TrackManager()
    return track_manager.download_track_v2(trackid, batch, local_path)

def write_newest_batch(track_id, batch):
    track_manager = TrackManager()
    return track_manager.wirte_batch_to_hbase(track_id, batch)

def get_newest_batch(track_id):
    track_manager = TrackManager()
    return track_manager.get_newest_batch(track_id)

def get_full_track_data(trackid, local_path):
    track_manager = TrackManager()
    return track_manager.download_full_track(trackid, local_path)

def wirte_full_batch(track_id, batch):
    track_manager = TrackManager()
    return track_manager.wirte_full_batch_to_hbase(track_id, batch)

def get_full_track_newest_batch(track_id):
    track_manager = TrackManager()
    return track_manager.get_full_track_newest_batch(track_id)

def save_track_path(row_key, track_path):
    track_manager = TrackManager()
    return track_manager.save_track_path(row_key, track_path)

def save_full_track_path(row_key, track_path):
    track_manager = TrackManager()
    return track_manager.save_full_track_path(row_key, track_path)

def element_save_track_path(rowkey, track_path):
    track_manager = TrackManager()
    return track_manager.element_save_track_path(rowkey, track_path)

def element_get_track_path(rowkey):
    track_manager = TrackManager()
    return track_manager.element_get_track_path(rowkey)

def element_get_track_data(track_id ,batch ,target_path):
    track_manager = TrackManager()
    return track_manager.element_get_track_data(track_id, batch, target_path)

def element_get_full_track_data(track_id ,target_path):
    track_manager = TrackManager()
    return track_manager.element_get_full_track_data(track_id, target_path)

def element_write_newest_batch(track_id, batch):
    track_manager = TrackManager()
    return track_manager.element_write_batch_to_hbase(track_id, batch)

def element_get_newest_batch(track_id):                                                                                         
    track_manager = TrackManager()
    return track_manager.element_get_newest_batch(track_id)

def main():
    pass

if __name__=='__main__':
    #import base_conf
    track_manager = TrackManager()
    print element_get_track_data('1003263_20180623082322963', '201406393_1', './')
    #print get_track_data_v2('1027016_20180913104303011', '1057330_1', './')
    #print track_manager.download_full_track('26_20180623055908071', '.')
    #print element_get_track_data('1003263_20180623082322963', '201406393_1', './')
    #print element_get_full_track_data('1003259_20180621153951549' ,'.')
    #exit(4)
    #print track_manager.element_get_track_path('1000022_20180730151053997-!!!:201607709_1')
    #print track_manager.element_get_newest_batch('26_20180623081235990')
    #print element_get_full_track_data('26_20180623081235990' , '.')
    #print element_get_track_data('26_20180623081235990', '400059635_1' , './')
    #print element_get_track_data('400047388_2019013012055203', '400052426_1','./')
    #print element_get_track_data('400047388_20190130120552039', '400052426_1','./')
    #main()
    #print track_manager.wirte_batch_to_hbase('99999_20180701073630032','99999_3')
    #print write_newest_batch('99999_20180701073630032','99999_1')
    #print batch_to_hbase('9999', '9999_1')
    #print track_manager.get_newest_batch('99999_20180701073630032')
    #print get_track_data('1017985_20180806104812175','./')
    #print track_manager.get_full_track_newest_batch('9999_128827264')
    #print get_full_track_newest_batch('400051009_20190131123235077')
    #print track_manager.get_full_track_path('400051009_20190131123235077', '400051089_1')
    #print get_full_track_newest_batch('1003259_20180621153951549')
    #print wirte_full_batch('9999_128827264', '999_1')
    #print 'success!'
    #print host_ip
    #print element_get_track_data('1104821_20180624061215589', '333335_1', './')
    #print element_get_track_path('_SUCCESS-333335_1')
    #print element_save_track_path('201377986_20190222105506469-9999_1' ,'/user/hwl/test/201377986_20190222105506469.gz')
