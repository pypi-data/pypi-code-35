#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import re
import sys
import service_config
from bases.log import *
from redis_utils import RedisUtils

redis_utils = RedisUtils()
hadoop_home = '/opt/hadoop-3.1.0'
dfs_path_prefix = '/production/service-jaguar'
def get_job_id_from_name(name):
    cmd = "%s/bin/hadoop job -list 2>/dev/null | grep %s | awk '{print $1}'" % (hadoop_home, name)
    logger().info('get job id cmd : %s ', cmd )
    res = os.popen(cmd).read()
    return res

def get_job_progress_from_name(name):
    cmd = "%s/bin/hadoop job -list 2>/dev/null | grep %s | awk '{print $1}' | xargs %s/bin/hadoop job -status 2>/dev/null | grep complet" % (
        hadoop_home,
        name,
        hadoop_home
    )
    res = os.popen(cmd).read()

    result = []
    for line in res.split('\n'):
        if "map" in line or 'reduce' in line:
            segs = line.split('completion:')
            pro_map = round(float(segs[1].strip()), 2)
            result.append(pro_map)

    logger().info('hadoop[%s] progress[%s]', name, str(result))
    return result

def hrm(dfs_path):
    cmd = "%s/bin/hadoop fs -rm -r -f %s" % (
        hadoop_home,
        dfs_path_prefix + dfs_path
    )
    print "hrm cmd is : " + cmd
    #return os.system(cmd)==0

def exist(dfs_path):
    cmd = "%s/bin/hadoop fs -test -e %s" % (
        hadoop_home,
        dfs_path
    )
    print cmd
    return os.system(cmd) == 0

def hdu(dfs_path):
    cmd = "%s/bin/hadoop fs -du -s %s | awk '{print $1}'" % (
        hadoop_home,
        dfs_path
    )
    print cmd
    return os.popen(cmd).read().strip()
    
def hput(local_path, dfs_path):
    cmd = "%s/bin/hadoop fs -put -f %s %s" % (hadoop_home, local_path, dfs_path)
    print 'hadoop cmd : ' + cmd
    res = os.system(cmd)==0
    print res
    return res


def hmkdir(dfs_path, recursive=True):
    cmd_fmt = "%s/bin/hadoop fs -mkdir "
    if recursive:
        cmd_fmt += '-p'
    cmd_fmt += ' %s'
    cmd = cmd_fmt % (hadoop_home, dfs_path)
    logger().info('hadoop cmd: ' + cmd)
    res = os.system(cmd) == 0
    return res


def hcat(dfs_path_file):
    cmd = "%s/bin/hadoop fs -cat %s" % (hadoop_home, dfs_path_file)
    res = os.popen(cmd).read().strip()
    return res

def getTrackPaths(taskId):
    task_path = redis_utils.get_task_path(taskId)
    logger().info('taskId : %s get task_path : %s ', taskId, str(task_path))
    track_path_list = []
    cmd = "%s/bin/hadoop fs -ls %s/track | awk '{print $8}' | cat -A" % (hadoop_home, task_path)
    logger().info('taskId : %s , get TrackPath cmd : %s ', taskId, cmd)
    for line in os.popen(cmd):
        line = line.strip()[:-1]
        if re.match("track[0-9]+", line.split(os.sep)[-1])!=None:
            track_path_list.append(line)
    return track_path_list


def main():
    print get_job_id_from_name('R_200705574_1-1')
    #print exist(sys.argv[1])
    #print get_job_progress_from_name(sys.argv[1])
    #print exist(sys.argv[0])

if __name__ == '__main__':
    main()
