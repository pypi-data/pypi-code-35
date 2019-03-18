import socket
from pathlib import Path

import requests
from docopt import docopt as docoptinit

from . import util

register_kong_doc = """
Usage:
    register_kong [options]
    
Options:
    --name=<name>
    --uris=<uris>
    --hosts=<hosts>
    --port=<port>
    --ip=<ip>
    --region=<region>
    --preserve-host
    --upstream-suffix=<sufix>
    --timeout=<timeout>            [default: 3]
    --kube-svc=<svc>               Ip comes from kube service. This will overwrite --ip option
"""


def register_kong(argv):
    docopt = docoptinit(register_kong_doc, argv)
    print(docopt)
    name = docopt['--name']
    uris = docopt['--uris']
    port = docopt['--port']
    hosts = docopt['--hosts']
    timeout = float(docopt['--timeout'])
    region = docopt['--region']
    upstream_suffix = docopt['--upstream-suffix'] or ''
    preserve = docopt['--preserve-host']
    if region == 'alihz':
        url = 'http://alihz-master-0.internal.qbtrade.org:8001/apis'
    elif region == 'alihk-stage':
        url = 'http://alihk-stage-0.qbtrade.org:8001/apis'
    elif region == 'alihk-0-14':
        url = 'http://alihk-master.qbtrade.org:9001/apis'
    else:
        url = 'http://kong-admin.qbtrade.org/apis'
    kube_svc = docopt['--kube-svc']
    if not docopt['--ip']:
        ip = socket.gethostbyname(socket.gethostname())
    else:
        ip = docopt['--ip']
    if kube_svc:
        p = Path('~/.qb/jwt').expanduser()
        qbjwt = p.read_text().strip()
        print(qbjwt[:10])
        assert p.is_file()
        res = util.must_success(
            requests.get, url='http://api.qbtrade.org/kube/default/services', headers={'jwt': qbjwt})
        for item in res.json():
            if item['metadata']['name'] == kube_svc:
                ip = item['spec']['clusterIP']
                break
        else:
            raise ValueError('service not found')
    r = requests.delete('{url}/{name}'.format(url=url, name=name), timeout=timeout)
    print('delete', r.text)
    seconds = 1000
    data = {
        'name': name,
        'upstream_url': 'http://{}:{}{}'.format(ip, port, upstream_suffix),
        'upstream_connect_timeout': seconds,
        'upstream_read_timeout': 30 * seconds,
        'upstream_send_timeout': 30 * seconds,
    }

    if hosts:
        data['hosts'] = hosts
    if uris:
        data['uris'] = uris
        data['strip_uri'] = 'true'
    if preserve:
        data['preserve_host'] = 'true'

    print('post', url, data)
    r = util.must_success(requests.post, url, data=data)
    print('add', r.text, ip)
