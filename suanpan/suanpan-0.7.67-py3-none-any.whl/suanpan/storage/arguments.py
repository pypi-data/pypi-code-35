# coding=utf-8
from __future__ import print_function

import numpy as np
from sklearn2pmml import sklearn2pmml
from sklearn.externals import joblib

from suanpan import objects, path
from suanpan.arguments import Arg
from suanpan.components import Result
from suanpan.storage import storage
from suanpan.utils import csv, json


class StorageArg(Arg):
    def getOutputTmpValue(self, *args):
        return storage.delimiter.join(args)


class File(StorageArg):
    FILENAME = "file"
    FILETYPE = None

    def __init__(self, key, **kwargs):
        # kwargs.update(required=False)
        fileName = kwargs.pop("name", self.FILENAME)
        fileType = kwargs.pop("type", self.FILETYPE)
        self.fileName = (
            "{}.{}".format(fileName, fileType.lower()) if fileType else fileName
        )
        super(File, self).__init__(key, **kwargs)

    @property
    def isSet(self):
        return True

    def load(self, args):
        self.objectPrefix = super(File, self).load(args)
        self.objectName = (
            storage.storagePathJoin(self.objectPrefix, self.fileName)
            if self.objectPrefix
            else None
        )
        self.filePath = (
            storage.getPathInTempStore(self.objectName) if self.objectName else None
        )
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
    # def __init__(self, key, **kwargs):
    #     kwargs.update(required=False)
    #     super(Folder, self).__init__(key, **kwargs)

    @property
    def isSet(self):
        return True

    def load(self, args):
        self.folderName = super(Folder, self).load(args)
        self.folderPath = (
            storage.getPathInTempStore(self.folderName) if self.folderName else None
        )
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
        return super(Json, self).save(context, Result(self.filePath))


class Csv(Data):
    FILETYPE = "csv"

    def format(self, context):
        super(Csv, self).format(context)
        self.value = csv.load(self.filePath)
        return self.value

    def save(self, context, result):
        csv.dump(result.value, self.filePath)
        return super(Csv, self).save(context, Result(self.filePath))


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
        return super(Npy, self).save(context, Result(self.filePath))


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

    def load(self, args):
        self.objectPrefix = super(SklearnModel, self).load(args)
        self.filePath = (
            storage.getPathInTempStore(self.objectPrefix) if self.objectPrefix else None
        )
        if self.filePath:
            path.safeMkdirs(self.filePath)

        self.pmmlPath = (
            storage.localPathJoin(self.filePath, "pmml") if self.filePath else None
        )
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
        sklearn2pmml(
            pipelineModel,
            storage.localPathJoin(self.pmmlPath, "model.pmml"),
            with_repr=True,
        )

        storage.upload(self.objectPrefix, self.filePath)
        return self.objectPrefix


class PmmlModel(Arg):
    def __init__(self, key, **kwargs):
        kwargs.update(required=True)
        super(PmmlModel, self).__init__(key, **kwargs)

    def load(self, args):
        self.objectPrefix = super(PmmlModel, self).load(args)
        self.filePath = (
            storage.getPathInTempStore(self.objectPrefix) if self.objectPrefix else None
        )
        if self.filePath:
            path.safeMkdirs(self.filePath)

        self.pmmlPath = (
            storage.localPathJoin(self.filePath, "pmml") if self.filePath else None
        )
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
