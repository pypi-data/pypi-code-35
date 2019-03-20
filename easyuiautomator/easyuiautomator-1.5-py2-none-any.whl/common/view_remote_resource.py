#coding=utf-8
'''
Created on 2017年7月12日

@author: Administrator
'''
import threading, json
import requests

root_path = "http://172.16.12.46/raptor_back/web/testresources/"
sim = root_path + "sim"
wifi = root_path + "wifi"

class ViewRemoteResource(object):
    '''查看服务器远程资源，用于自动化辅助能力
    '''
    headers={"Content-Type": "application/json"}
    __instance = None
    __mutex = threading.Lock()
    
    def __init__(self):
        pass
    
    @staticmethod
    def getInstance():
        """Return a single instance of ViewRemoteResource object """
        if (ViewRemoteResource.__instance == None):
            ViewRemoteResource.__mutex.acquire()
            if (ViewRemoteResource.__instance == None):
                ViewRemoteResource.__instance = ViewRemoteResource()
            ViewRemoteResource.__mutex.release()
        return ViewRemoteResource.__instance
    
    def _query_data(self, url, data):
        '''查询服务器数据'''
        r = requests.post(url, data=json.dumps(data), headers=self.headers, timeout=10)
        return json.loads(r.content)
    
    def getSimInfo(self, iccid):
        data = {'imsi': iccid}
        return self._query_data(sim, data)
    
    def getWifiHotInfo(self):
        '''获取wifi热点信息'''
        data = {'ip': "tmp"}
        return self._query_data(wifi, data)
    
if __name__ == '__main__':
    print ViewRemoteResource.getInstance().getWifiHotInfo()['data']
        