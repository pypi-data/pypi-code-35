# coding=utf-8
from __future__ import print_function

import numpy as np
from sklearn2pmml import sklearn2pmml
from sklearn.externals import joblib

from suanpan import path
from suanpan.arguments import Arg
from suanpan.components import Result
from suanpan.log import logger as log
from suanpan.storage import storage
from suanpan.utils import csv, json


class StorageArg(Arg):
    def getOutputTmpValue(self, *args):
        return storage.delimiter.join(args)


class File(StorageArg):
    FILENAME = "file"
    FILETYPE = None

    def __init__(self, key, **kwargs):
        fileName = kwargs.pop("name", self.FILENAME)
        fileType = kwargs.pop("type", self.FILETYPE)
        self.fileName = (
            "{}.{}".format(fileName, fileType.lower()) if fileType else fileName
        )
        self.objectPrefix = None
        self.objectName = None
        self.filePath = None
        super(File, self).__init__(key, **kwargs)

    @property
    def isSet(self):
        return True

    def load(self, args):
        self.objectPrefix = super(File, self).load(args)
        if self.objectPrefix:
            self.objectName = storage.storagePathJoin(self.objectPrefix, self.fileName)
        if self.objectName:
            self.filePath = storage.getPathInTempStore(self.objectName)
        if self.filePath:
            path.safeMkdirsForFile(self.filePath)
        self.value = self.filePath
        return self.filePath

    def format(self, context):
        if self.filePath:
            storage.download(self.objectName, self.filePath)
        return self.filePath

    def save(self, context, result):
        filePath = result.value
        storage.upload(self.objectName, filePath)
        self.logSaved(self.objectName)
        return self.objectPrefix


class Folder(StorageArg):
    def __init__(self, key, **kwargs):
        super(Folder, self).__init__(key, **kwargs)
        self.folderName = None
        self.folderPath = None

    @property
    def isSet(self):
        return True

    def load(self, args):
        self.folderName = super(Folder, self).load(args)
        if self.folderName:
            self.folderPath = storage.getPathInTempStore(self.folderName)
        if self.folderPath:
            path.safeMkdirs(self.folderPath)
        self.value = self.folderPath
        return self.folderPath

    def format(self, context):
        if self.folderPath:
            storage.download(self.folderName, self.folderPath)
        return self.folderPath

    def clean(self, context):
        if self.folderPath:
            path.empty(self.folderPath)
        return self.folderPath

    def save(self, context, result):
        folderPath = result.value
        storage.upload(self.folderName, folderPath)
        self.logSaved(self.folderName)
        return self.folderName


class Data(File):
    FILENAME = "data"


class Json(Data):
    FILETYPE = "json"

    def format(self, context):
        super(Json, self).format(context)
        self.value = json.load(self.filePath)
        return self.value

    def save(self, context, result):
        json.dump(result.value, self.filePath)
        return super(Json, self).save(context, Result(value=self.filePath))


class Csv(Data):
    FILETYPE = "csv"

    def format(self, context):
        super(Csv, self).format(context)
        self.value = csv.load(self.filePath)
        return self.value

    def save(self, context, result):
        csv.dump(result.value, self.filePath)
        return super(Csv, self).save(context, Result(value=self.filePath))


class Table(Csv):
    pass


class Npy(Data):
    FILETYPE = "npy"

    def format(self, context):
        super(Npy, self).format(context)
        self.value = np.load(self.filePath)
        return self.value

    def save(self, context, result):
        np.save(self.filePath, result.value)
        return super(Npy, self).save(context, Result(value=self.filePath))


class Model(File):
    FILENAME = "model"


class H5Model(Model):
    FILETYPE = "h5"


class Checkpoint(Model):
    FILETYPE = "ckpt"


class JsonModel(Model):
    FILETYPE = "json"


class SklearnModel(Arg):
    def __init__(self, key, **kwargs):
        kwargs.update(required=True)
        super(SklearnModel, self).__init__(key, **kwargs)
        self.objectPrefix = None
        self.filePath = None
        self.pmmlPath = None

    def load(self, args):
        self.objectPrefix = super(SklearnModel, self).load(args)
        if self.objectPrefix:
            self.filePath = storage.getPathInTempStore(self.objectPrefix)
        if self.filePath:
            path.safeMkdirs(self.filePath)
            self.pmmlPath = storage.localPathJoin(self.filePath, "pmml")
        if self.pmmlPath:
            path.safeMkdirs(self.pmmlPath)

        self.value = self.filePath
        return self.filePath

    def format(self, context):
        super(SklearnModel, self).format(context)
        storage.download(self.objectPrefix, self.filePath)

        modelPath = storage.localPathJoin(self.filePath, "model.model")
        self.value = joblib.load(modelPath)
        return self.value

    def save(self, context, result):
        pipelineModel = result.value
        joblib.dump(result.value, storage.localPathJoin(self.filePath, "model.model"))

        try:
            sklearn2pmml(
                pipelineModel,
                storage.localPathJoin(self.pmmlPath, "model.pmml"),
                with_repr=True,
            )
        except RuntimeError as e:
            log.warn("Could not convert sklearn model to pmml, cause: {}".format(e))
            log.warn("Skip this process for now")

        storage.upload(self.objectPrefix, self.filePath)
        return self.objectPrefix


class PmmlModel(Arg):
    def __init__(self, key, **kwargs):
        kwargs.update(required=True)
        super(PmmlModel, self).__init__(key, **kwargs)
        self.objectPrefix = None
        self.filePath = None
        self.pmmlPath = None

    def load(self, args):
        self.objectPrefix = super(PmmlModel, self).load(args)
        if self.objectPrefix:
            self.filePath = storage.getPathInTempStore(self.objectPrefix)
        if self.filePath:
            path.safeMkdirs(self.filePath)
            self.pmmlPath = storage.localPathJoin(self.filePath, "pmml")
        if self.pmmlPath:
            path.safeMkdirs(self.pmmlPath)

        self.value = self.filePath
        return self.filePath

    def format(self, context):
        super(PmmlModel, self).format(context)
        storage.download(self.objectPrefix, self.filePath)

        pmmlPath = storage.localPathJoin(self.pmmlPath, "model.pmml")
        with open(pmmlPath, "r") as file:
            self.value = file.read()

        return self.value
