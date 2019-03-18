# coding=utf-8
from __future__ import print_function

import argparse
import os

from suanpan import objects, utils
from suanpan.log import logger
from suanpan.utils import json

DEFAULT_ARG_VALUE_DELIMITER = "::"
DEFAULT_ACTUAL_ARG_VALUE_DELIMITER = "_"
DEFAULT_MAX_VALUE_LENGTH = 120


class Arg(objects.HasName):
    ARG_VALUE_DELIMITER = DEFAULT_ARG_VALUE_DELIMITER
    ACTUAL_ARG_VALUE_DELIMITER = DEFAULT_ACTUAL_ARG_VALUE_DELIMITER
    MAX_VALUE_LENGTH = DEFAULT_MAX_VALUE_LENGTH

    def __init__(self, key, **kwargs):
        if "default" in kwargs:
            kwargs.update(required=False)

        self.argkey = key
        self.key = self.fixGlobalKey(key)
        self.value = None
        self.type = kwargs.pop("type", str)
        self.required = kwargs.pop("required", False)
        self.default = kwargs.pop("default", None)

        self.kwargs = self.cleanParams(kwargs)
        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def isSet(self):
        return self.required or self.default != self.value

    def addParserArguments(self, parser, required=None, default=None):
        required = self.required if required is None else required
        default = default or self.default
        return parser.add_argument(
            "--{}".format(self.argkey),
            type=self.typeDecorator(self.type),
            required=required,
            default=default,
            **self.kwargs
        )

    def addGlobalParserArguments(self, parser, required=None, default=None):
        default = os.environ.get(self.envKeyFormat(self.key), default or self.default)
        self.addParserArguments(parser, required=required, default=default)

    def typeDecorator(self, typeFunc):
        def _decorator(value):
            return getattr(self, "default", None) if value == "" else typeFunc(value)

        return _decorator

    def load(self, args):
        self.value = getattr(args, self.key)
        self.value = self.fixArgValue(self.value)
        self.logLoaded(self.value)
        return self.value

    def format(self, context):
        return self.value

    def clean(self, context):
        return self.value

    def save(self, context, result):
        self.logSaved(result.value)
        return result.value

    def cleanParams(self, params):
        return {k: v for k, v in params.items() if not k.startswith("_")}

    def logLoaded(self, value):
        logger.info(
            "({type}) {key} loaded: {value}".format(
                type=self.name,
                key=self.key,
                value=utils.shorten(value, maxlen=self.MAX_VALUE_LENGTH),
            )
        )

    def logSaved(self, value):
        logger.info(
            "({type}) {key} saved: {value}".format(
                type=self.name,
                key=self.key,
                value=utils.shorten(value, maxlen=self.MAX_VALUE_LENGTH),
            )
        )

    def fixArgValue(self, value):
        return value

    def fixGlobalKey(self, key):
        return key.replace("-", "_")

    def envKeyFormat(self, key):
        return self.fixGlobalKey(key).upper()


class String(Arg):
    def __init__(self, key, **kwargs):
        super(String, self).__init__(key, type=str, **kwargs)


class Int(Arg):
    def __init__(self, key, **kwargs):
        super(Int, self).__init__(key, type=int, **kwargs)


class Float(Arg):
    def __init__(self, key, **kwargs):
        super(Float, self).__init__(key, type=float, **kwargs)


class Bool(Arg):
    def __init__(self, key, **kwargs):
        kwargs.update(default=False)
        super(Bool, self).__init__(key, type=type(self).str2bool, **kwargs)

    @classmethod
    def str2bool(cls, string):
        if string.lower() in ("yes", "true", "t", "y", "1"):
            return True
        elif string.lower() in ("no", "false", "f", "n", "0"):
            return False
        else:
            raise argparse.ArgumentTypeError("Boolean value expected.")


class List(Arg):
    def __init__(self, key, **kwargs):
        super(List, self).__init__(key, type=type(self).str2list, **kwargs)

    @classmethod
    def str2list(cls, string):
        try:
            return [cls.transform(i.strip()) for i in string.split(",") if i.strip()]
        except Exception:
            raise argparse.ArgumentTypeError("{} value expected.".format(cls.__name__))

    @classmethod
    def transform(cls, item):
        return item


class ListOfString(List):
    pass


class ListOfInt(List):
    @classmethod
    def transform(cls, item):
        return int(item)


class ListOfFloat(List):
    @classmethod
    def transform(cls, item):
        return float(item)


class ListOfBool(List):
    @classmethod
    def transform(cls, item):
        return Bool.str2bool(item)


class Json(String):
    def __init__(self, key, **kwargs):
        if "default" in kwargs:
            kwargs["default"] = json.dumps(kwargs["default"])
        super(Json, self).__init__(key, **kwargs)

    def format(self, context):
        if self.value is not None:
            self.value = json.loads(self.value)
        return self.value

    def save(self, context, result):
        self.logSaved(result.value)
        return json.dumps(result.value)


class BoolOrInt(Arg):
    def __init__(self, key, **kwargs):
        super(BoolOrInt, self).__init__(key, type=type(self).str2boolint, **kwargs)

    @classmethod
    def str2boolint(cls, string):
        if string.lower() in ("yes", "true", "t", "y", "1"):
            return True
        elif string.lower() in ("no", "false", "f", "n", "0"):
            return False
        else:
            return int(string)
