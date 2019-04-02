#!/usr/bin/env python
# -*- coding: utf-8 -*-

import redis_pool
import json
import sys
import os
import service_config
from singleton import singleton

#project_name = service_config.GET_CONF("service", "project_name")
project_name = 'jaguar'

@singleton
class RedisUtils():
    def __init__(self):
        self.r = redis_pool.Pool().get('ir_server')
    
    # task queue, 0: start task 1: stop task
    def queue_push(self, data, which):
        if which==0:
            return self.r.lpush(service_config.GET_CONF("redis", project_name + "_cmd_start_queue"), data)
        elif which==1:
            return self.r.lpush(service_config.GET_CONF("redis", project_name + "_cmd_stop_queue"), data)

    def queue_len(self, which):
        if which==0:
            return self.r.llen(service_config.GET_CONF("redis", project_name + "_cmd_start_queue"))
        elif which==1:
            return self.r.llen(service_config.GET_CONF("redis", project_name + "_cmd_stop_queue"))

    def queue_pop(self, which):
        if which==0:
            return self.r.rpop(service_config.GET_CONF("redis", project_name + "_cmd_start_queue"))
        elif which==1:
            return self.r.rpop(service_config.GET_CONF("redis", project_name + "_cmd_stop_queue"))

    # start task pid
    def set_start_pid(self, seq, start_pid):
        return self.r.hset(service_config.GET_CONF("redis", project_name + "_start_pid"), seq, start_pid)

    def get_start_pid(self, seq):
        return self.r.hget(service_config.GET_CONF("redis", project_name + "_start_pid"), seq)

    def rem_start_pid(self, seq):
        return self.r.hdel(service_config.GET_CONF("redis", project_name + "_start_pid"), seq)

    def set_cur_name(self, seq, cur_name):
        return self.r.hset(service_config.GET_CONF("redis", project_name + "_cur_name"), seq, cur_name)

    def get_cur_name(self, seq):
        return self.r.hget(service_config.GET_CONF("redis", project_name + "_cur_name"), seq)

    def rem_cur_name(self, seq):
        return self.r.hdel(service_config.GET_CONF("redis", project_name + "_cur_name"), seq)

    # start task state
    def set_state(self, seq, state):                                                                                              
        return self.r.hset(service_config.GET_CONF("redis", project_name + "_state"), seq, state)

    def get_state(self, seq):
        return self.r.hget(service_config.GET_CONF("redis", project_name + "_state"), seq)

    def rem_state(self, seq):
        return self.r.hdel(service_config.GET_CONF("redis", project_name + "_state"), seq)

    # running start task
    def add_running(self, seq):
        return self.r.sadd(service_config.GET_CONF("redis", project_name + "_running"), seq)

    def rem_running(self, seq):
        return self.r.srem(service_config.GET_CONF("redis", project_name + "_running"), seq)

    def scard_running(self):
        return self.r.scard(service_config.GET_CONF("redis", project_name + "_running"))

    def smembers_running(self):
        return self.r.smembers(service_config.GET_CONF("redis", project_name + "_running"))

    # running stop task
    def add_running_stop(self, seq):
        return self.r.sadd(service_config.GET_CONF("redis", project_name + "_running_stop"), seq)

    def rem_running_stop(self, seq):
        return self.r.srem(service_config.GET_CONF("redis", project_name + "_running_stop"), seq)

    def scard_running_stop(self):
        return self.r.scard(service_config.GET_CONF("redis", project_name + "_running_stop"))

    def smembers_running_stop(self):
        return self.r.smembers(service_config.GET_CONF("redis", project_name + "_running_stop"))

    def clear(self):
        self.r.delete(service_config.GET_CONF("redis", project_name + "_start_pid"))
        self.r.delete(service_config.GET_CONF("redis", project_name + "_state"))
        self.r.delete(service_config.GET_CONF("redis", project_name + "_running"))
        self.r.delete(service_config.GET_CONF("redis", project_name + "_running_stop"))
        self.r.delete(service_config.GET_CONF("redis", project_name + "_cur_name"))
        return True


    #process pid
    def set_process_pid(self, process_name, pid):
        return self.r.hset(service_config.GET_CONF("redis", project_name + "_process_pid"), process_name, pid)
    
    def set_type(self, project_id, task_type):
        return self.r.hset("jaguar_type", project_id, task_type)
    
    def get_type(self, project_id):
        return self.r.hget("jaguar_type", project_id)

    def get_process_pid(self):
        return self.r.hgetall(service_config.GET_CONF("redis", project_name + "_process_pid"))

    def set_auto_status(self, project_id, track_id, statu_data):
        return self.r.hset(project_id + "_auto", track_id, statu_data)
    
    def get_auto_status(self, project_id, track_id):
        ret = self.r.hget(project_id + "_auto", track_id) 
        if not ret:
            print >> sys.stderr, 'no res, return 0'
            return 0
        return ret
    
    def get_all_auto_status(self, project_id):
        return self.r.hgetall(project_id + "_auto")
    
    def rem_auto_status(self, project_id):
        return self.r.delete(project_id + "_auto")

    def set_fusion_status(self, project_id, track_id, statu_data):
        return self.r.hset(project_id + "_fusion", track_id, statu_data)
    
    def get_fusion_status(self, project_id, fusion_id):
        ret = self.r.hget(project_id + "_fusion", fusion_id)
        if not ret:
            print >> sys.stderr, 'no res, return 0'
            return 0
        return ret 
    
    def get_all_fusion_status(self, project_id):
        return self.r.hgetall(project_id + "_fusion")
    
    def rem_fusion_status(self, project_id):
        return self.r.delete(project_id + "_fusion")

    def push_status(self, project_id, task_id, _type, status):
        data = '%s-%s-%s-%s' % (project_id, task_id, _type, status)
        self.r.lpush('stat_queue', data)

    def pop_status(self):
        data = self.r.rpop('stat_queue')
        if data: return data.split('-')
        else: return None



def main():
    q = RedisUtils()
    print q.set_auto_status('5', '26_20180623062901409', 1)
    print q.get_auto_status('5', '26_20180623062901409')
    #print q.set_auto_status('5', '26_20180623062901409', 0)
    print q.get_fusion_status('5', '26_201806230629014094') 
    exit(4)
    exit(2)
    print q.set_state("3", "running")
    data = json.dumps({"id":"auto_111","track_id":"track_111","fid":["xxx","yyy"],"status":"processing"})
    print q.get_auto_status("123", "123_99999_12345")
    print q.set_auto_status("123", "123_99999_54321", data)
    all_info =  q.get_all_auto_status("123")
    print type(all_info)
    print all_info
    exit(1)
    fusion_data = '{"id":"fusion_111","fid":"xxxxx","track_ids":["track_111","track_222"],"status":"cpp binary failed"}'
    print q.set_fusion_status("999", "999_00000_12345", fusion_data)
    print q.get_fusion_status("999", "999_00000_12345")

if __name__ == '__main__':

    q = RedisUtils()
    print q.push_status('p1', '1', 'auto', '0')
    print q.push_status('p1', '2', 'fusion','0')
    print q.push_status('p1', '3', 'position', '0')
    print q.push_status('p1', '4', 'traffic' ,'0')
    print q.pop_status()
    print q.pop_status()
    print q.pop_status()
    print q.pop_status()
    print q.pop_status()
    print q.pop_status()
    print q.pop_status()
    print q.pop_status()
