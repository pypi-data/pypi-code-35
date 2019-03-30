# -*- coding: utf-8 -*-

import zlib
import base64

import msgpack
import itsdangerous


class CookieManSerializer(object):
    '''
    Signed compressed session cookie serializer.

    This class implements the following:
    - Messagepack python object serialization.
    - Signature check using itsdangerous.TimestampSigner.
    - Compression using python's standard zlib.
    - URL-safe base64 encoding (to http header issues).
    '''

    signer_class = itsdangerous.TimestampSigner
    bad_sicnature_exception = itsdangerous.BadSignature

    def __init__(self, secret, salt):
        '''
        :param secret:
        :type secret:
        :param salt:
        :type salt:
        '''
        self.signer = self.signer_class(secret, salt=salt)

    def dumps(self, data):
        '''
        Get serialized representation of given object.

        :param data: serializable object
        :type data: object
        :returns: serialized data
        :rtype: bytes
        '''
        dumped = msgpack.packb(data, use_bin_type=True)
        signed = self.signer.sign(dumped)
        compressed = zlib.compress(signed)
        return base64.urlsafe_b64encode(compressed)

    def loads(self, data, max_age=None):
        '''
        Get object from serialized data.

        :param data: serialized data
        :type data: bytes
        :returns: deserialized object
        :rtype: object
        '''
        decoded = base64.urlsafe_b64decode(data)
        decompressed = zlib.decompress(decoded)
        signed = self.signer.unsign(decompressed, max_age=max_age)
        return msgpack.unpackb(signed, raw=False)
