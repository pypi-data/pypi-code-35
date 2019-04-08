#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json

class MessageException(Exception):
    pass

class RequestException(Exception):
    pass


class FollowUp:

    def __init__(self, action, value=None):

        self.action = action
        self.value = value


class StatusCode:
    STATUS_OK = 'OK'
    STATUS_WARNING = 'WARNING'
    STATUS_ERROR = 'ERROR'


class MessageType:
    TYPE_REQUEST = 'REQUEST'
    TYPE_RESPONSE = 'RESPONSE'
    TYPE_INFO = 'INFO'


class SerializableMessage:
    """ General class for serializable messages """

    def __init__(self):
        self.type = None
        self.data = None

    def set_data(self, data):
        """ set data """
        if isinstance(data, dict) and self._is_serializable(data):
            self.data = data
        else:
            raise RequestException('Sorry, data must be a serializable dict')

    def _is_serializable(self, data):
        """ check if data is json-serializable """
        try:
            json.dumps(data)
            return True
        except:
            return False

    def obj_to_dict(self):
        """ converts to dict """

        data_dict = {}
        data_dict['type'] = self.type
        data_dict['data'] = self.data

        return data_dict

    def encode(self, MSG_LEN):
        """ converts to fixed-length byte data """

        data_dict = self.obj_to_dict()
        byte_data = json.dumps(data_dict).encode('utf-8')
        # zero padding
        byte_data += b'0' * (MSG_LEN - len(byte_data))
        return byte_data

    @staticmethod
    def encoded_to_dict(data):
        try:
            # convert to string
            padded_data = data.decode('utf-8')
            # remove zero padding
            sep = padded_data.find('}0')+1
            data_dict = json.loads(padded_data[:sep])
        except:
            raise MessageException('Message cannot be decoded')

        return data_dict


class Request(SerializableMessage):
    """ Request object """

    def __init__(self):
        super().__init__()
        self.type = MessageType.TYPE_REQUEST
        self.classname = None
        self.classpath = None

    def set_classname(self, classname):
        """ class to invoke for fulfilling the request """
        if isinstance(classname, str):
            self.classname = classname
        else:
            raise RequestException('Classname must be a string')

    def set_classpath(self, classpath):
        """ class to invoke for fulfilling the request """
        if isinstance(classpath, str):
            self.classpath = classpath
        else:
            raise RequestException('Classpath must be a string')

    def obj_to_dict(self):
        """ converts to dict """

        data_dict = super().obj_to_dict()
        data_dict['classname'] = self.classname
        data_dict['classpath'] = self.classpath

        return data_dict

    @staticmethod
    def decode(encoded):

        data_dict = SerializableMessage.encoded_to_dict(encoded)

        request = Request()
        request.classname = data_dict.get('classname')
        request.classpath = data_dict.get('classpath')
        request.data = data_dict.get('data')

        return request


class Response(SerializableMessage):
    """ Response object """

    def __init__(self):
        super().__init__()
        self.type = MessageType.TYPE_RESPONSE
        self.status = None

    def set_status(self, status):
        """ set status code """
        if status not in (StatusCode.STATUS_OK, StatusCode.STATUS_WARNING, StatusCode.STATUS_ERROR):
            raise ResponseException('Status code not supported')
        self.status = status

    def obj_to_dict(self):
        """ converts to dict """

        data_dict = super().obj_to_dict()
        data_dict['status'] = self.status

        return data_dict

    @staticmethod
    def decode(encoded):

        data_dict = SerializableMessage.encoded_to_dict(encoded)

        response = Response()
        response.status = data_dict.get('status')
        response.data = data_dict.get('data')

        return response


if __name__ == '__main__':

    response = Response()
    response.set_status(StatusCode.STATUS_OK)
    #response.set_description('tutto ok')

    data = {'0': 'pippo', '1': {'a': 'pluto', 'b': 'minnie'}}
    response.set_data(data)

    encoded = response.encode(1024)
    print(encoded)
    decoded = Response.decode(encoded)
    print(decoded.obj_to_dict())
    #encoded = ByteMessage(1024).encode(response)
    #decoded = ByteMessage(1024).decode(encoded)
