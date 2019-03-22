
class requests_wrapper():
    client = None

    def __init__(self, *arg, **args):
        pass
    

    def fetch(self, url, body, method, headers, **request_parameters):
        if(method == 'GET'):
            return requests_body_wrapper(self.client.get(url, data=body, headers=headers))
        else:
            return requests_body_wrapper(self.client.post(url, data=body, headers=headers))


class requests_body_wrapper(object):

    def __init__(self, res):
        self.body = res.text.encode()