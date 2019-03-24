# -*- coding:utf-8 -*-

import bottle
from rest import Kmux, KmuxHTTPRequest, KmuxHTTPResponse, KmuxHandler


@bottle.route('/<path:re:.*>', method=['GET', 'PUT', 'POST', 'HEAD', 'PATCH', 'DELETE', 'OPTIONS'])
def kmux_bottle_handler(path):
    request = KmuxHTTPRequest(
        method=bottle.request.method,
        url=bottle.request.url,
        headers=dict(bottle.request.headers),
        body=bottle.request.body.read(),
        request_uuid=None,
        request_time=None,
    )
    handler = KmuxHandler.create_handler(request)
    assert isinstance(handler, KmuxHandler)
    handler.handle()
    response = handler.get_response()
    assert isinstance(response, KmuxHTTPResponse)
    return bottle.HTTPResponse(response.get_chunk(), response.get_status(), response.get_headers())


class KmuxBottleApplication(object):
    def start(self, port=8080, host=None):
        Kmux().init()
        port = int(port)
        host = '0.0.0.0' if host is None else host
        bottle.run(port=port, host=host)


if __name__ == '__main__':
    from example import *
    app = KmuxBottleApplication()
    app.start()
