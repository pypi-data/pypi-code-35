import sys
import json
import http.server
import socketserver
import argparse
import logging
#import re
from os import listdir
from os.path import isfile, join

#PATH_RE = r'\/\w{1,50}'

class HttpServer(http.server.BaseHTTPRequestHandler):
    Env = None
   
    def do_GET(self):
        log = logging.getLogger()
    
        if self.path == '/favicon.ico':
            self.send_response(404)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(str('Favicon not configured').encode())

        if self.path == '/.update':
            log.info('Update triggered')
            self.send_response(204)            
            self.end_headers()
    
        if not self.path or self.path == '/':
            p = self.Env.path
            onlyfiles = [f for f in listdir(p) if isfile(join(p, f)) and not f.startswith('.')]

            self.send_response(200)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(', '.join(onlyfiles).encode())
            return
    
        try:
            #if not re.fullmatch(PATH_RE, self.path):
            #    raise UserWarning(f'Requested path "{self.path}" is invalid')
                
            #file_path = (self.Env.path or '') + self.path + '.json'
            
            file_path = self.Env.path + self.path
            s = ''
            try:
                with open(file_path) as inp:
                    #s = inp.read()
                    for line in inp:
                        line = line.strip()
                        if line and not line.startswith('//'):
                            s += line
            except Exception as ex:
                raise UserWarning(ex)
                    
            # reload rules
            try:
                with open(self.Env.file) as inp:
                    rules = json.loads(inp.read())
            except json.decoder.JSONDecodeError as ex:
                raise UserWarning(f'Processing rules file is invalid: {ex}')
            
            except FileNotFoundError:
                rules = None
                log.debug(f'.rules files not specified => no processing of input')

            if rules:
                if 'subst' in rules:
                    for x, y in rules['subst']:
                        s = s.replace(x, y)
                else:
                    log.debug(f'Node "subst" not found in rules file.')
                    
            try:
                obj = json.loads(s)
            except json.decoder.JSONDecodeError as ex:
                raise UserWarning(f'Produced file invalid: {ex}. File: {s}')

            result = self._process(obj, rules) if rules else obj

            resp = json.dumps(result, indent=0 if self.Env.zip else 2)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(resp.encode())
                
        except UserWarning as ex:
            log.error('%s: %s', self.path, str(ex))
            
            self.send_response(404)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(str(ex).encode())

    def _process(self, d, rules):
        log = logging.getLogger()
        
        # Put values
        if 'values' in rules:
            for k, v in rules['values'].items():
                items = k.split('.')
                parent = d
                for x in items[:-1]:
                    if x in parent:
                        parent = parent[x]
                    else:
                        parent[x] = {}
                        parent = parent[x]
                parent[items[-1]] = v
        else:
            log.debug(f'Node "values" not found in rules file.')

        # Includes
        if 'include' in rules:
            for dest, file_name in rules['include'].items():
                try:
                    with open(self.Env.path + '/' + file_name) as inp:
                        j = json.loads(inp.read())
                except (json.decoder.JSONDecodeError, FileNotFoundError) as ex:
                    raise UserWarning(f'Included file {file_name} is invalid: {ex}')
                
                items = dest.split('.')
                parent = d
                for x in items[:-1]:
                    if x in parent:
                        parent = parent[x]
                    else:
                        parent[x] = {}
                        parent = parent[x]
                parent[items[-1]] = j
        
        return d

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--iface', help='Listen interface', default='')
    parser.add_argument('--port', help='Listen TCP/IP port', default=80, type=int)
    parser.add_argument('--file', help='Configuration file')
    parser.add_argument('--path', help='Files location', default='.')
    parser.add_argument('--zip', help='Make response condensed', action='store_true')
    env = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    log = logging.getLogger()
    
    # Test conf
    if not env.file:
        env.file = env.path + '/.rules.json'
    
    HttpServer.Env = env

    try:
        with socketserver.TCPServer((env.iface, env.port), HttpServer) as httpd:
            log.info(f'Listen on {env.iface or "0.0.0.0"}:{env.port}')
            httpd.serve_forever()
    except KeyboardInterrupt:
        return 0

sys.exit(main())