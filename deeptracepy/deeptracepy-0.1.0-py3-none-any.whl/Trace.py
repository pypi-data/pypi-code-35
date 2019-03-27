import uuid
from datetime import datetime

class Trace():
    def __init__(self, config, req, resp):
        self.data = None
        self.config = config
        self.req = req
        self.resp = resp

    def factory(self):
        self.data = {
            'tags': self.config['tags'],
        }

        self.set_trace_idx(self.req)
        self.set_request(self.req)
        self.set_response(self.resp)

        # TODO: The response timestamp must be when the request starts
        self.data['response']['timestamp'] = str(datetime.now())
        self.data['request']['timestamp'] = str(datetime.now())
        return self
        
    def set_request(self, req):
        self.data['request'] = self.__get_request_data(req)

    def set_response(self, resp):
        self.resp.headers['id'] = self.data['id']
        self.data['response'] = self.___response(resp)
    
    def ___response(self, resp):
        return {
            'status': resp.status_code,
            'headers': dict(resp.headers),
            'body': 'None' #str(resp.data.decode("utf-8").replace("'", '"'))
        }

    def set_trace_idx(self, req):
        contact_id = req.headers['parentid']
        req_id = str(uuid.uuid4())

        self.data['id'] = req_id
        self.data['parentid'] = contact_id,
        self.data['parentid'] = self.data['parentid'][0] \
            if type(self.data['parentid']) is tuple else self.data['parentid']
        self.data['rootid'] = req_id if contact_id is None else contact_id

    def __get_request_data(self, req):
        return {
            'ip': req.remote_addr,
            'method': req.method,
            'uri': req.url,
            'headers': dict(req.headers),
            'body': 'None' #str(resp.data.decode("utf-8").replace("'", '"'))
        }
    