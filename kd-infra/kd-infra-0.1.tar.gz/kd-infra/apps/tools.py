# -*- coding:utf-8 -*-
import os
import sys
import json
import urllib
import urllib2
import service_config
import requests
import time
#from dump_status import StatusDumper 
from redis_utils import RedisUtils
from log import logger
import StringIO
import gzip


def send_alert(message,title):
    quiet = service_config.GET_CONF('service','alert_pause')
    if quiet == 'True':
        print sys.stderr, 'alert pause, will not send alert'
        return False
    alert_url = service_config.GET_CONF('service','alert_url')
    #alert_url = 'http://op-01.gzproduction.com:9527/api/msg/send'
    title = title
    alert_type = 2
    formdata = {
	"title": title,
	"message": message,
	"alert_type": alert_type,
        "to_party": 20
    }
    data = urllib.urlencode(formdata)
    req = urllib2.Request(alert_url, data = data)
    ret = urllib2.urlopen(req)
    res = ret.read()
    response = json.loads(res)
    return '0' == response['code']

def set_status_to_hbase(project_id, taskid, status, returncode, _type):
    for i in range(3):
        ret = __set_status_to_hbase(project_id, taskid, status, returncode, _type)
        logger().info('time [%d] insert status to hbase ret [%s]', i + 1, ret)
        if ret:
            logger().info('insert status to hbase success')
            return True
    return False

def __set_status_to_hbase(project_id, taskid, status, returncode, _type):
    set_status_url = service_config.GET_CONF("service", "set_status_url")
    payload = {}
    key = 'jaguar_status_%s_%s_%s' % (project_id, _type, taskid)
    payload["key"] = key 
    value = '%s#%s' % (status, returncode)
    payload["value"] = value
    #logger().info('post key [%s] value [%s]', key, value)
    res = requests.post(set_status_url, data=payload)
    if res.status_code != 200:
        logger().error("return code is not 200")
        return False
    try:
        jdata = res.json()
        logger().info('key [%s] jdata [%s]', key, str(jdata))
    except Exception, e:
        import traceback
        traceback.print_exc(e)
        return False
    return jdata['code'] == '0'

def get_status_from_hbase(project_id, taskid, _type):
    start_time = time.time()
    get_status_url = service_config.GET_CONF("service", "get_status_url")
    payload = {}
    key = '%s_%s_%s' % (project_id, _type, taskid)
    payload["key"] = key 
    res = requests.get(get_status_url, data=payload)
    if res.status_code != 200:
        logger().error("return code is not 200 vs %s", str(res.status_code))
        return False
    try:
        jdata = res.json()
        if jdata['code'] != '0':
            return False
        end_time = time.time()
        const_time = end_time - start_time
        #logger().info('get info key [%s], value [%s] const time [%s]', 
        #                key, str(jdata['result']), const_time)
        return jdata['result']
    except Exception, e:
        import traceback
        traceback.print_exc(e)

def get_track_info(taskid):
    get_status_url = service_config.GET_CONF("service", "get_track_info_url")
    payload = {}
    payload["track_id"] = taskid
    res = requests.post(get_status_url, data=payload)
    if res.status_code != 200:
        logger().error("return code is not 200 vs %s", str(res.status_code))
        return False
    try:
        jdata = res.json()
    except Exception, e:
        import traceback
        traceback.print_exc(e)
        return False
    return json.dumps(jdata['result'])

def get_all_status(project_id):
    get_status_url = service_config.GET_CONF("service", "get_all_status_url")
    payload = {}
    payload["projectId"] = project_id
    res = requests.post(get_status_url, data=payload)
    if res.status_code != 200:
        logger().error("return code is not 200 vs %s", str(res.status_code))
        return False
    try:
        jdata = res.json()
    except Exception, e:
        import traceback
        traceback.print_exc(e)
        return False
    return json.dumps(jdata['result'])

def get_version():
    #url = 'http://op-01.gzproduction.com:9527/api/service_version/get_all'
    url = service_config.GET_CONF("service", "service_versions_url")
    print url
    res = requests.post(url)
    if res.status_code != 200:
        logger().error("return code is not 200 vs %s", str(res.status_code))
        return None
    try:
        jdata = res.json()
        re = jdata['result']
        results = {}
        if len(re['fusion']) > 0 and len(re['auto']) > 0 and len(re['ground']) > 0 and len(re['pole']) >0:
            results['fusion'] = re['fusion'][0]
            results['auto'] = re['auto'][0]
            results['ground'] = re['ground'][0]
            results['pole'] = re['pole'][0]
        else:
            logger().error("version fusion: %s, auto: %s, ground: %s, pole: %s",  ( re['fusion'],re['auto'], re['ground'], re['pole'] ))
            return None
    except Exception, e:
        import traceback
        traceback.print_exc(e)
        return None
    return results

def build_log_link():
    CONTAINER_ID = os.getenv('CONTAINER_ID')
    NM_HOST = os.getenv('NM_HOST')
    mapred_task_id = os.getenv('mapred_task_id')
    NM_PORT = os.getenv('NM_PORT')
    base_url = ('http://hm-001:19888/jobhistory/logs'
                '/%s:%s/%s/%s/hadoop/stderr/') % (NM_HOST, NM_PORT, CONTAINER_ID,
                        mapred_task_id)
    logger().info('jobhistory url : %s', base_url)
    return base_url

#status = start or stop
def dotting(project_id, taskid, _type, status):
    for i in range(3):
        ret = __dotting(project_id, taskid, _type, status)
        logger().info('time [%d] insert status to hbase ret [%s]', i + 1, ret)
        if ret:
            logger().info('insert status to hbase success')
            return True
        time.sleep(3)
    return False

def __dotting(project_id, taskid, _type, status):
    if status == 'start':
        dotting_url = service_config.GET_CONF('service','dotting_url')
    else:
        dotting_url = service_config.GET_CONF('service','dotting_stop_url')
    #payload = {}
    #payload['pid'] = project_id 
    #payload['stage'] = _type
    #payload['taskid'] = taskid
    try:
        dotting_url = '%s?pid=%s&stage=%s&taskid=%s' % (dotting_url, project_id, _type, taskid)
        logger().info('post pid [%s] stage [%s], taskid [%s], url [%s] status [%s]', 
                    project_id, _type, taskid, dotting_url, status)
        res = requests.post(dotting_url)
    except:
        logger().error("get a exception")
        return False
    if res.status_code != 200:
        logger().error("return code is not 200 vs %s", str(res.status_code))
        logger().error('error info [%s]', str(res.json))
        return False
    try:
        jdata = res.json()
        logger().info('jdata [%s]', str(jdata))
    except Exception, e:
        import traceback
        traceback.print_exc(e)
        return False
    return jdata['code'] == '0'

def dotting_all(project_id, data):
    for i in range(3):
        ret = __dotting_all(project_id, data)
        logger().info('time [%d] insert status to hbase ret [%s]', i + 1, ret)
        if ret:
            logger().info('insert status to hbase success')
            return True
        time.sleep(3)
    return False

def __dotting_all(project_id, data):
    dotting_url = service_config.GET_CONF('service','dotting_all_url')
    taskids = json.dumps(data) 
    dotting_url = '%s?pid=%s' % (dotting_url, project_id)
    logger().info('post pid [%s] taskids [%s], url [%s]', 
                    project_id, str(taskids), dotting_url)
    try:
        res = requests.post(dotting_url, data=taskids)
    except:
        logger().info('__dotting_all get an exception')
        return False
    if res.status_code != 200:
        logger().error("return code is not 200 vs %s", str(res.status_code))
        logger().error('error info [%s]', str(res.json))
        return False
    try:
        jdata = res.json()
        logger().info('jdata [%s]', str(jdata))
    except Exception, e:
        import traceback
        traceback.print_exc(e)
        return False
    return jdata['code'] == '0'
    
def dotting_stage(project_id, stage):
    for i in range(3):
        ret = __dotting_stage(project_id, stage)
        logger().info('time [%d] insert status to hbase ret [%s]', i + 1, ret)
        if ret:
            logger().info('insert status to hbase success')
            return True
        time.sleep(3)
    return False

def __dotting_stage(project_id, stage):
    dotting_url = service_config.GET_CONF('service','dotting_stage_url')
    print dotting_url
    dotting_url = '%s?pid=%s&stage=%s' % (dotting_url, project_id, stage)
    logger().info('post pid [%s] url [%s], stage [%s]', 
                    project_id, dotting_url, stage)
    try:
        res = requests.post(dotting_url)
    except:
        logger().info('__dotting_stage get an exception')
        return False
    if res.status_code != 200:
        logger().error("return code is not 200 vs %s", str(res.status_code))
        logger().error('error info [%s]', str(res.json))
        return False
    try:
        jdata = res.json()
        logger().info('jdata [%s]', str(jdata))
    except Exception, e:
        import traceback
        traceback.print_exc(e)
        return False
    return jdata['code'] == '0'

def gzip_compress(buf):
    out = StringIO.StringIO()
    with gzip.GzipFile(fileobj=out, mode="w") as f:
        f.write(buf)
    return out.getvalue()

def get_cpp_mem(taskid):
    show_cmd = 'ps aux | grep -v grep| grep %s | awk \'{print $6}\'' % taskid
    print show_cmd
    data = os.popen(show_cmd, 'r').read()
    ret = data.strip().split('\n')[1:]
    for line in ret:
        print line

def main():
    #print dotting_stage('300000210', 'auto')
    #exit(4) 
    get_cpp_mem('400115432')
    #print dotting('1', '1', 'auto', 'stop')
    exit(4) 
    print dotting_all('300000210',{})
    exit(4) 
    #print send_alert("6666", "bpl")
    #print set_status_to_hbase('300000138', '300005683', '0', '0', 'traffic')
    #print get_status_from_hbase('300000138', '300005683', 'traffic')
    #print get_track_info('1026990_20180905143247856')
    #print build_log_link()
    #print get_all_status('567')

if __name__ == '__main__':
    main()
    print(get_version())
