from django.db import connections
import datetime
import json #for logging
import socket #for logging
import httpagentparser #for logging
from getmac import getmac #for logging

# REQUIRED (pip install get-mac, pip install httpagentparser)

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def get_mac():
    mac = getmac.get_mac_address()
    return mac

def get_mac_from_ip(ipnya):
    mac = getmac.get_mac_address(ip=ipnya, network_request=True)
    return mac

def detectBrowser(request):
    agent = request.environ.get('HTTP_USER_AGENT')
    browser = httpagentparser.detect(agent)
    user_browser = ''
    browser_ver = ''
    os = ''
    os_ver = ''
    
    if not browser:
        user_browser = agent.split('/')[0]
        browser_ver= ''
        os= ''
        os_ver= ''
    else:
        user_browser = browser['browser']['name']
        browser_ver = browser['browser']['version']
        os = browser['os']['name']
        os_ver = browser['os']['version']

    data = {
        'user_browser':user_browser,
        'browser_ver':browser_ver,
        'os':os,
        'os_ver':os_ver,            
    }
    return data

def get_queries(db_name):
    Q_2019 = connections[db_name].queries
    log_queries = {}

    for i in range(len(Q_2019)):
        log_queries[i] = Q_2019[i]['sql']
    return log_queries

def get_username_log(request, user_name):
    usernamenya = request.session.get(user_name,'')
    return usernamenya

def logging(request,user_name,db_name):
    log_tgl_sekarang = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # ----------- LOGGING -----------
    log_username = get_username_log(request, user_name)
    log_url = request.path
    log_ip = get_ip()
    log_mac = get_mac_from_ip(get_ip())
    log_tgl_akses = log_tgl_sekarang
    log_browser = detectBrowser(request)['user_browser']
    log_browser_ver = detectBrowser(request)['browser_ver']
    log_os = detectBrowser(request)['os']
    log_os_ver = detectBrowser(request)['os_ver']   
    log_queriess = get_queries(db_name)
    # ----------- END OF LOGGING -----------

    log_json = {
        'log_username':log_username,
        'log_url':log_url,
        'log_ip':log_ip,
        'log_mac':log_mac,
        'log_tgl_akses':log_tgl_akses,
        'log_browser':log_browser,
        'log_browser_ver':log_browser_ver,
        'log_os':log_os,
        'log_os_ver':log_os_ver,
        'log_queries':log_queriess,
    }
    
    return json.dumps(log_json)