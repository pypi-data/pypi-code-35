from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import argparse
import subprocess
import uuid
import json
import gzip

from flask import Flask, request, jsonify, Response
import yaml

from py_eureka_client.eureka_client import RegistryClient as Shit
class EurekaRegistryClient(Shit):
    def _Shit__try_all_eureka_server(self, fun):
        # try:
            # super(EurekaRegistryClient, self).__try_all_eureka_server(fun=fun)
        # except:
            # print('error')
            
        raise('fack111')

import msgpack
import StringIO

parser  = argparse.ArgumentParser()
parser.add_argument("--debug_flask", default=False, help="Enable debug for flask or not(eg. False)", type=bool)
parser.add_argument("--log_level", default="info", help="The log level(eg. info)")

parser.add_argument("--host", default="0.0.0.0", help="The host of the server(eg. 0.0.0.0)")
parser.add_argument("--port", default=5000, help="The port of the server(eg. 5000)", type=int)
parser.add_argument("--config", required=True, help="Path of the yaml model definition")
parser.add_argument("--discovery", default="http://quaeroml.com:8761/eureka/", help="Receives a comma delimited list of hosts where to find the eureka discovery service")
parser.add_argument("--join", default=True, help="Decides if join the cluster or not")
parser.add_argument("--tunnel", default=True, help="Decides if do tunneling")

args    = parser.parse_args( sys.argv[1:] )

import logging
logger_eureka           = logging.getLogger('EurekaClient')
logger_eureka.disabled  = True

logger_flask            = logging.getLogger('werkzeug')
logger_flask.disabled   = True


logging.basicConfig(
    level   = eval( 'logging.' + args.log_level.upper() ), 
    format  = '%(asctime)s %(levelname)-8s %(message)s', 
    datefmt = '%Y-%m-%d %H:%M:%S')
    

APP_HOST    = str(uuid.uuid4())[:8] + '.lt.quaeroml.com' # 3 collisions in 100k
LT_PORT     = 3000
MODEL_CFG   = yaml.load( open(args.config, 'r') ) 
APP_NAME    = MODEL_CFG['name'] + '-v' + MODEL_CFG['version']
MODEL       = None

app         = Flask(__name__)
from flask.logging import default_handler
app.logger.removeHandler(default_handler)

def gzipencode(data, compresslevel=9):
    out = StringIO.StringIO()
    f   = gzip.GzipFile(fileobj=out, mode='w', compresslevel=compresslevel)
    f.write(data)
    f.close()
    
    return out.getvalue()
    
def gzipdecode(raw):
    buff = StringIO.StringIO(raw)
    data = gzip.GzipFile(fileobj=buff, mode='r')
    return data.read()
    
def is_application(type):
    return request.headers.get('Content-Type').lower() == ('application/' + type)
    
def inputize():
    data = request.data
    
    if request.headers.get('Content-Encoding') == 'gzip':
        data = gzipdecode(data)
      
    input = None
    if is_application('json'):
        input = json.loads(data)
    
    if is_application('msgpack'):
        input = msgpack.unpackb(data, raw=False)
        
    if not input:
        raise Exception('Unable to decode request data')
                
    return input
    
def outputize(datao):
    response                            = Response()
    response.status_code                = 200
    response.headers['Content-Type']    = request.headers.get('Content-Type')
    
    if is_application('json'):
        datao = json.dumps(datao)
        
    if is_application('msgpack'):
        datao = msgpack.packb(datao, use_bin_type=True )
            
    if request.headers.get('Content-Encoding') == 'gzip':
        datao = gzipencode(datao)
        
        response.headers['Content-Encoding'] = 'gzip'
        response.headers['Vary'] = 'Accept-Encoding'

    response.data                       = datao
    response.headers['Content-Length']  = len(response.data)
    
    return response
    
def model_load():
    global MODEL
    model       = MODEL_CFG['model']
    model_type  = model['type']
    
    if model_type.lower() == "h2o":
        try:
            from .ModelH2o import ModelH2o
        except:
            from ModelH2o import ModelH2o
            
        MODEL = ModelH2o(MODEL_CFG)
     
     
            
@app.route("/score", methods=["POST"])
def score(): 
    global MODEL
    input   = inputize()
    result  = MODEL.inference(input)
    datao   = {"success" : True, 'data' : result}
    
    return outputize(datao)

@app.route("/echo", methods=["POST"])
def echo(): 
    input   = inputize()
    datao   = {"success" : True, 'data' : input}
    
    return outputize(datao)
    
@app.route("/")
def root():
    return ping()
    
@app.route("/ping")
def ping():
    return ":) " + str(args.port)
 
@app.errorhandler(Exception)
def all_exception_handler(e):
    logging.error(e)
    
    out = {"success" : False, 'error' : str(e)}

    return ( jsonify(out), 500 )
        
def main():
    model_load()
        
    from healthcheck import HealthCheck, EnvironmentDump
    health      = HealthCheck(app, "/health")
    envdump     = EnvironmentDump(app, "/info")

    import flask_monitoringdashboard as dashboard
    dashboard.bind(app) #/dashboard
    
    localtunnel = None
    if args.tunnel or args.join:
        fh          = open('procout', "w")
        comm        = [ 'python', '3rdparty/pagekite.py', '--nocrashreport', '--clean', '--frontend=' + APP_HOST + ':' + str(LT_PORT), '--service_on=http:' + APP_HOST + ':localhost: ' + str(args.port) + ':2MagicDav1d' ]
        localtunnel = subprocess.Popen(comm) #, stdout = fh, stderr = fh)
        fh.close()
    
    cluster = None
    if args.join:
        eurekac = EurekaRegistryClient(
            eureka_server=args.discovery, 
            instance_port=LT_PORT, 
            instance_host=APP_HOST, 
            app_name=APP_NAME)
            
        eurekac.start()
    
    app.run(host=args.host, port=args.port, threaded=True, debug=args.debug_flask)
    
    if args.join:
        eurekac.stop()
        
    if localtunnel:
        localtunnel.terminate()
    
if __name__ == "__main__":
  main()
