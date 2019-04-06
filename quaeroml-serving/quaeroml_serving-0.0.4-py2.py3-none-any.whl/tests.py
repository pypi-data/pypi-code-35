import subprocess
import json
import time

import StringIO
import gzip
import requests 
import msgpack

HOST        = 'http://localhost'
PORT        = '6000'
ENDPOINT    = HOST + ':' + PORT + '/echo'

def gzipencode(data, compresslevel=9):
    out = StringIO.StringIO()
    f   = gzip.GzipFile(fileobj=out, mode='w', compresslevel=compresslevel)
    f.write(data)
    f.close()
    
    return out.getvalue()
    
def launch_h2o():
    proc_args   = ['python', 'server.py', '--port='+PORT, '--config', 'examples/H2O_glm_prostate.yml']
    proc        = subprocess.Popen(proc_args)

    time.sleep(20)
    return proc
            
def h2o_json():
    json_   = '{"data": [ [1,65,1,2,1,1.4,0,6], [2,72,1,3,2,6.7,0,7], [3,70,1,1,2,4.9,0,6] ], "keys": ["ID","AGE","RACE","DPROS","DCAPS","PSA","VOL","GLEASON"]}'
    data    = json.loads(json_)
    
    headers = {'Content-Type': 'application/json'}
    r       = requests.post(url = ENDPOINT, data = json_, headers=headers) 
    
    datao   = json.loads(r.content) 
    
    assert(data == datao['data'])

def h2o_json_gzip():
    json_   = '{"data": [ [1,65,1,2,1,1.4,0,6], [2,72,1,3,2,6.7,0,7], [3,70,1,1,2,4.9,0,6] ], "keys": ["ID","AGE","RACE","DPROS","DCAPS","PSA","VOL","GLEASON"]}'
    data    = json.loads(json_)

    headers = {'Content-Type': 'application/json', 'Content-Encoding': 'gzip'}
    r       = requests.post(url = ENDPOINT, data = gzipencode(json_), headers=headers) 
    
    datao   = json.loads(r.content) 
    
    assert(data == datao['data'])
    
def h2o_messagepack():
    json_   = '{"data": [ [1,65,1,2,1,1.4,0,6], [2,72,1,3,2,6.7,0,7], [3,70,1,1,2,4.9,0,6] ], "keys": ["ID","AGE","RACE","DPROS","DCAPS","PSA","VOL","GLEASON"]}'
    data    = json.loads(json_) 
    datap   = msgpack.packb(data, use_bin_type=True)
    
    headers = {'Content-Type': 'application/msgpack'}
    r       = requests.post(url = ENDPOINT, data = datap, headers=headers) 
    
    datao   = msgpack.unpackb(r.content, raw=False) 
    
    assert(data == datao['data'])


def main():
    server = launch_h2o()
    h2o_json()
    h2o_json_gzip()
    h2o_messagepack()
    
    server.terminate()
    
if __name__ == "__main__":
  main()