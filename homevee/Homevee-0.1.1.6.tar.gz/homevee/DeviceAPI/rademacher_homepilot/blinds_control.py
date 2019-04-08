#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import urllib.request, urllib.parse, urllib.error

from homevee.Helper import Logger
from homevee.Manager.gateway import get_gateway
from homevee.gateway_keys import RADEMACHER_HOMEPILOT

def control_blinds(id, goto, db):
    data = get_gateway(RADEMACHER_HOMEPILOT, db)
    ip = data['IP']

    url = "http://"+ip+"/deviceajax.do?cid=9&did="+str(id)+"&goto="+str(goto)+"&command=0"

    Logger.log(url)

    response = urllib.request.urlopen(url).read()

    data = json.loads(response)

    if(data['status'] != 'uisuccess'):
        return {'result': 'error'}

    Logger.log(response)

    with db:
        cur = db.cursor()

        cur.execute("UPDATE HOMEPILOT_BLIND_CONTROL SET LAST_POS = :pos WHERE ID == :id",
                    {'pos': goto, 'id': id})
    return {'result': 'ok'}