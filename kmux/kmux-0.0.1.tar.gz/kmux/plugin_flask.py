# -*- coding:utf-8 -*-

import flask
from rest import Kmux, KmuxHTTPRequest, KmuxHTTPResponse, KmuxHandler

flask_app = flask.Flask('__KMUX__')


@flask_app.route('/<path:path>', methods=['GET', 'PUT', 'POST', 'HEAD', 'PATCH', 'DELETE', 'OPTIONS'])
def kmux_flask_handler(path):
    request = KmuxHTTPRequest(
        method=flask.request.method,
        url=flask.request.url,
        headers=dict(flask.request.headers),
        body=flask.request.data,
        request_uuid=None,
        request_time=None,
    )
    handler = KmuxHandler.create_handler(request)
    assert isinstance(handler, KmuxHandler)
    handler.handle()
    response = handler.get_response()
    assert isinstance(response, KmuxHTTPResponse)
    return flask.make_response(response.get_chunk(), response.get_status(), response.headers)


class KmuxFlaskApplication(object):
    def start(self, port=8080, host=None):
        Kmux().init()
        port = int(port)
        host = '0.0.0.0' if host is None else host
        flask_app.run(port=port, host=host)


if __name__ == '__main__':
    from example import *
    app = KmuxFlaskApplication()
    app.start()
