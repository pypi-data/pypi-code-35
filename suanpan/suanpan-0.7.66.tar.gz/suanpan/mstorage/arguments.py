# coding=utf-8
from __future__ import print_function

from suanpan.arguments import Arg
from suanpan.mstorage import mstorage
from suanpan.utils import csv, json, npy, pickle


class MStorageArg(Arg):
    def format(self, context):
        if self.value:
            self.value = self.getValue()
        return self.value

    def save(self, context, result):
        obj = result.value
        self.setValue(obj)
        self.logSaved(self.value)
        return self.value

    def fixArgValue(self, value):
        return (
            value.replace(self.ARG_VALUE_DELIMITER, "_")
            if isinstance(value, str)
            else value
        )


class Pickle(MStorageArg):
    def getValue(self):
        data = mstorage.mget(self.value)
        return pickle.loads(data)

    def setValue(self, obj):
        data = pickle.dumps(obj)
        return mstorage.set(self.value, data)


class Any(Pickle):
    pass


class Npy(MStorageArg):
    def getValue(self):
        data = mstorage.mget(self.value)
        params = json.loads(data["md"].decode())
        params["data"] = data["data"]
        return npy.loads(params)

    def setValue(self, obj):
        params = npy.dumps(obj)
        npybytes = params.pop("data")
        data = {"md": json.dumps(params), "data": npybytes}
        return mstorage.mset(self.value, data)


class Csv(Npy):
    def getValue(self):
        data = mstorage.get(self.value)
        return csv.loads(data)

    def setValue(self, dataframe):
        data = csv.dumps(dataframe)
        return mstorage.set(self.value, data)


class Table(Csv):
    pass
