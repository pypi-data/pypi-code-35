#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import os
import requests


if os.getenv('PYTHONPATH') and 'py_path_managers/projects' in os.getenv('PYTHONPATH'):
    import jaguar_v2
    jaguar_v2.sys_append_paths()

from bases.log import logger
from bases.service_config import GET_CONF

def append(file_path, data):
    f = open(file_path, 'a')
    f.write(data)
    f.write('\n')
    f.close()

def write(file_path, data):
    f = open(file_path, 'w')
    f.write(data)
    f.write('\n')
    f.close()

def read(file_path):
    raw_lines = [line.strip() for line in open(file_path)]
    lines = [line for line in raw_lines if line]
    return lines

class Client(object):
    def __init__(self, queue_name, url):
        self.__queue_name = queue_name
        self.__push_url = url + '/citroen/push?queue=%s' % self.__queue_name
        self.__pop_url = url + '/citroen/pop?queue=%s' % self.__queue_name
        self.__len_url = url + '/citroen/length?queue=%s' % self.__queue_name
        self.__popall_url = url + '/citroen/popall?queue=%s' % self.__queue_name
        self.__delete_url = url + '/citroen/delete?queue=%s' % self.__queue_name

    # param data could be a string or a list of string
    def push(self, data, project_id, priority=GET_CONF('priority', 'NORMAL')):
        push_url = self.__push_url
        push_url += '&project_id=%s&priority=%s' % (project_id, priority)
        res = requests.post(push_url, data=data)
        if res.status_code != 200:
            logger().error("return code is not 200")
            return False
        jdata = res.json()
        if jdata['code'] != '0':
            logger().error("json code is[%s]", str(jdata['code']))
            return False
        logger().info('push succ. queue: %s, proj: %s, priority: %s, data: %s',
                self.__queue_name, project_id, priority, data[:100])
        return True

    def pop(self, priority):
        pop_url = self.__pop_url
        pop_url += '&priority=%s' % (priority)
        res = requests.get(pop_url)
        if res.status_code != 200:
            logger().error("return code is not 200")
            return None
        jdata = res.json()
        if jdata['code'] != '0':
            logger().error("json code is[%s]", str(jdata['code']))
            return None

        logger().info('pop succ. queue: %s, priority: %s',
                self.__queue_name, priority)
        return jdata['result']

    def length(self, priority=''):
        len_url = self.__len_url
        len_url += '&priority=%s' % (priority)
        res = requests.get(len_url)
        if res.status_code != 200:
            raise Exception("return code is not 200")
        jdata = res.json()
        if jdata['code'] != '0':
            raise Exception("json code is[%s]", str(jdata['code']))

        logger().info('length succ. queue: %s, priority: %s, resp: %s',
                self.__queue_name, priority, jdata['result'])
        return jdata['result']

    def pop_all(self, priority=''):
        popall_url = self.__popall_url
        popall_url += '&priority=%s' % (priority)
        res = requests.get(popall_url)
        if res.status_code != 200:
            raise Exception("return code is not 200")
            return None
        jdata = res.json()
        if jdata['code'] != '0':
            raise Exception("json code is [%s]", str(jdata['code']))

        logger().info('pop all succ. queue: %s, priority: %s, resp: %s',
                self.__queue_name, priority, jdata['result'][:100])
        return jdata['result']

    def delete(self, project_id):
        delete_url = self.__delete_url + '&project_id=' + project_id
        res = requests.post(delete_url)
        if res.status_code != 200:
            logger().error("return code is not 200")
            return False
        jdata = res.json()
        if jdata['code'] != '0':
            logger().error("json code is[%s]", str(jdata['code']))
            return False

        logger().info('delete succ. queue: %s, proj: %s, resp: %s',
                self.__queue_name, project_id, jdata['result'][:100])
        return True


def get_client(name):
    return Client(name, url=GET_CONF('citroen', 'url'))
    
def main():
    VERY_HIGH = GET_CONF('priority', 'VERY_HIGH')
    HIGH = GET_CONF('priority', 'HIGH')
    NORMAL = GET_CONF('priority', 'NORMAL')

    client = get_client('test')
    print 'pop all:', client.pop_all()
    client.push('1', '12345', VERY_HIGH)
    client.push('2', '12345', HIGH)
    client.push('3', '12345', NORMAL)
    print 'pop all very high:', client.pop_all(VERY_HIGH)
    print 'pop all high:', client.pop_all(HIGH)
    print 'pop all normal:', client.pop_all(NORMAL)

    client.push('1', '12345', VERY_HIGH)
    client.push('2', '12345', HIGH)
    client.push('3', '12345', NORMAL)
    print 'len: ', client.length()
    print 'len very high: ', client.length(VERY_HIGH)
    print 'len high: ', client.length(HIGH)
    print 'len normal: ', client.length(NORMAL)
    print 'pop very high:', client.pop(VERY_HIGH)
    print 'pop high:', client.pop(HIGH)
    print 'pop normal:', client.pop(NORMAL)
    print 'len: ', client.length()
    exit(0)

    client.push('4', '23456')
    client.push('5', '23456')
    client.delete('23456')

    client.push('6', '45678')
    client.push('7', '45678')
    print 'pop:', client.pop()
    client.push('8', '56789')
    client.push('9', '00000')
    client.delete('45678')

    print 'pop all:', client.pop_all()
    print 'pop all:', client.pop_all()

 
if __name__ == '__main__':
    main()
