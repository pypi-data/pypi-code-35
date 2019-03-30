from flask import Flask, request, g

from .compression import Gzip, Deflate

# TODO: support gzip, compress, deflate, identity, br
COMPRESSIONS_LIST = (Gzip, Deflate)
SUPPORTED_ENCODINGS = {comp._encoding_name: comp for comp in COMPRESSIONS_LIST}


class FlaskCompressed:
    def __init__(self, app=None, encodings=SUPPORTED_ENCODINGS):
        self._encodings = encodings
        self._encoder_list = {}
        self.app = None

        if app is not None or not isinstance(app, Flask):
            self.init_app(app)

    def init_app(self, app: Flask):
        self.app = app

        self.app.before_request(self._before_request)
        self.app.after_request(self._after_request)

        for encoding in self._encodings:
            if encoding not in SUPPORTED_ENCODINGS:
                raise ValueError("Unsupported encodings : %s" % encoding)

            self._encoder_list[encoding] = SUPPORTED_ENCODINGS[encoding]

    def _get_encoding_list_from_request(self, content_encoding):
        if ',' in content_encoding:
            # if multiple encodings
            encodings = [x.strip() for x in content_encoding.split(',')]

            for index, encoding in enumerate(encodings):
                # not supported
                if encoding not in self._encodings:

                    # if index is 0 (first encoding)
                    if index == 0:
                        return None

                    raise ValueError('Unsupported encodings : %s' % encoding)
        else:
            if content_encoding not in self._encodings:
                # not supported
                return None

            encodings = [content_encoding]

        return encodings

    def _before_request(self):
        content_encoding = request.headers.get('Content-Encoding', '')
        encodings = self._get_encoding_list_from_request(content_encoding)
        if encodings is None:
            return

        decompressed = request.get_data()
        print(decompressed)
        for encoding in reversed(encodings):
            decompressed = \
                self._encoder_list[encoding].decompress(decompressed)

        g.body = decompressed

    def _after_request(self, response):
        return response
