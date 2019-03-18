# coding=utf-8
from __future__ import print_function

import argparse
import contextlib
import itertools
import time
import traceback
import uuid

from suanpan import arguments as baseargs
from suanpan import g, interfaces, objects
from suanpan.arguments import Bool, BoolOrInt, Float, Int, String
from suanpan.components import Arguments, Component
from suanpan.dw import dw
from suanpan.log import logger
from suanpan.mq import mq
from suanpan.mstorage import mstorage
from suanpan.storage import storage
from suanpan.utils import json


class Handler(Component):
    def __call__(self, steamObj, message, *arg, **kwargs):
        return self.run(steamObj, message, *arg, **kwargs)

    def run(self, steamObj, message, *arg, **kwargs):
        context = self.init(message)
        results = self.runFunc(steamObj, context, *arg, **kwargs)
        return self.save(context, results)

    def init(self, message):
        restArgs = self.getArgList(message)
        globalArgs, restArgs = self.loadGlobalArguments(restArgs=restArgs)
        self.initBase(globalArgs)
        context = self._getContext(message)
        args, restArgs = self.loadComponentArguments(context, restArgs=restArgs)
        setattr(context, "args", args)
        self.currentContext = context
        return self.currentContext

    @contextlib.contextmanager
    def context(self, message):
        yield objects.Context(message=message)

    def getArgList(self, message):
        inputArguments = itertools.chain(
            *[
                ["--{}".format(arg.key), message.get("in{}".format(i + 1))]
                for i, arg in enumerate(self.getArguments(include="inputs"))
                if message.get("in{}".format(i + 1)) is not None
            ]
        )
        outputArguments = itertools.chain(
            *[
                [
                    "--{}".format(arg.key),
                    self.getOutputTmpValue(message, "out{}".format(i + 1)),
                ]
                for i, arg in enumerate(self.getArguments(include="outputs"))
            ]
        )
        return list(itertools.chain(inputArguments, outputArguments))

    def saveOutputs(self, context, results):
        if results is not None:
            outputs = super(Handler, self).saveOutputs(context, results)
            outputs = self.formatAsOuts(outputs)
            outputs = self.stringifyOuts(outputs)
            return outputs

    def formatAsOuts(self, results):
        return {
            "out{}".format(i + 1): results[arg.key]
            for i, arg in enumerate(self.getArguments(include="outputs"))
            if results[arg.key] is not None
        }

    def stringifyOuts(self, outs):
        return {k: str(v) for k, v in outs.items()}

    def shortenRequestID(self, requestID):
        return requestID.replace("-", "")

    def getOutputTmpValue(self, message, output):
        shortRequestID = self.shortenRequestID(message["id"])
        return baseargs.DEFAULT_ARG_VALUE_DELIMITER.join(
            [
                g.USER_ID,  # pylint: disable=no-member
                g.APP_ID,  # pylint: disable=no-member
                g.NODE_ID,  # pylint: disable=no-member
                output,
                shortRequestID,
            ]
        )


class Stream(interfaces.HasBaseServices, interfaces.HasLogger, interfaces.HasDevMode):

    DEFAULT_STREAM_CALL = "call"
    STREAM_ARGUMENTS = [
        String("stream-user-id", required=True),
        String("stream-app-id", required=True),
        String("stream-node-id", required=True),
        String("stream-node-group", default="default"),
        String("stream-recv-queue", required=True),
        BoolOrInt("stream-recv-queue-block", default=False),
        Float("stream-recv-queue-delay", default=1.0),
        Int("stream-recv-queue-max-length", default=1000),
        Bool("stream-recv-queue-trim-immediately", default=False),
        Bool("stream-recv-queue-retry", default=False),
        Int("stream-recv-queue-retry-max-count", default=100),
        Float("stream-recv-queue-retry-timeout", default=1.0),
        Int("stream-recv-queue-retry-max-times", default=3),
        String("stream-send-queue", required=True),
        Int("stream-send-queue-max-length", default=1000),
        Bool("stream-send-queue-trim-immediately", default=False),
    ]

    def __init__(self):
        super(Stream, self).__init__()
        restArgs = self.getArgList()
        arguments, restArgs = self.loadGlobalArguments(restArgs=restArgs)
        self.args = Arguments(
            **{argument.key: argument.value for argument in arguments}
        )
        self.setOptions(self.args)
        self.setGlobals(self.args)
        self.setBaseServices(self.args)
        self.afterInit()

    def getGlobalArguments(self, *args, **kwargs):
        arguments = super(Stream, self).getGlobalArguments(*args, **kwargs)
        return arguments + self.STREAM_ARGUMENTS

    def generateRequestId(self):
        return uuid.uuid4().hex

    def formatMessage(self, message, msg, costTime=None):
        msgs = [message["id"], message.get("type", self.DEFAULT_STREAM_CALL), msg]
        if costTime is not None:
            msgs.insert(-1, "{}s".format(costTime))
        return " - ".join(msgs)

    def streamCall(self, message, *args, **kwargs):
        logger.info(self.formatMessage(message, msg="Start"))
        startTime = time.time()
        try:
            self.currentHandler = self.getHandler(message)
            outputs = self.currentHandler(self, message, *args, **kwargs) or {}
            endTime = time.time()
            costTime = round(endTime - startTime, 3)
            logger.info(self.formatMessage(message, msg="Done", costTime=costTime))
            if outputs:
                self.sendSuccessMessage(message, outputs)
        except Exception:
            tracebackInfo = traceback.format_exc()
            endTime = time.time()
            costTime = round(endTime - startTime, 3)
            logger.error(
                self.formatMessage(message, msg=tracebackInfo, costTime=costTime)
            )
            self.sendFailureMessage(message, tracebackInfo)

    def getHandler(self, message):
        streamCall = message.get("type", self.DEFAULT_STREAM_CALL)
        handler = getattr(self, streamCall, None)
        if not handler or not isinstance(handler, Handler):
            raise Exception(
                "Unknown stream handler: {}.{}".format(self.name, streamCall)
            )
        return handler

    def call(self, message, *args):
        raise NotImplementedError("Method not implemented!")

    def start(self):
        if self.options["recvQueueRetry"]:
            self.retryPendingMessages()
        for message in self.subscribe():
            self.currentMessage = message["data"]
            self.streamCall(self.currentMessage)

    def setDefaultMessageType(self, message):
        message["data"].setdefault("type", self.DEFAULT_STREAM_CALL)
        return message

    def getMessageExtraData(self, message):
        extra = message["data"].get("extra")
        extra = json.loads(extra) if extra else {}
        message["data"].update(extra=extra)
        return message

    def setOptions(self, args):
        self.options = self.defaultArgumentsFormat(args, self.STREAM_ARGUMENTS)
        return self.options

    def setGlobals(self, args):
        g.set("USER_ID", args.stream_user_id)
        g.set("APP_ID", args.stream_app_id)
        g.set("NODE_ID", args.stream_node_id)
        g.set("NODE_GROUP", args.stream_node_group)
        return g

    def afterInit(self):
        pass

    def createQueues(self, force=False):
        mq.createQueue(self.options["recvQueue"], force=force)
        mq.createQueue(self.options["sendQueue"], force=force)

    def subscribe(self, **kwargs):
        for message in mq.subscribeQueue(
            self.options["recvQueue"],
            group=self.options["nodeGroup"],
            consumer=self.options["nodeId"],
            block=self.options["recvQueueBlock"],
            delay=self.options["recvQueueDelay"],
            **kwargs
        ):
            message = self.setDefaultMessageType(message)
            message = self.getMessageExtraData(message)
            yield message

    def recv(self, **kwargs):
        return mq.recvMessages(
            self.options["recvQueue"],
            group=self.options["nodeId"],
            consumer=self.name,
            **kwargs
        )

    def _send(self, message, data, queue=None, extra=None):
        queue = queue or self.options["sendQueue"]
        message.setdefault("extra", {})
        message["extra"].update(extra or {})
        data = {
            "node_id": self.options["nodeId"],
            "request_id": message["id"],
            "type": message.get("type", self.DEFAULT_STREAM_CALL),
            "extra": json.dumps(message["extra"]),
            **data,
        }
        logger.debug("Send to `{}`: {}".format(queue, data))
        return mq.sendMessage(
            queue,
            data,
            maxlen=self.options["sendQueueMaxLength"],
            trimImmediately=self.options["sendQueueTrimImmediately"],
        )

    def sendSuccessMessage(self, message, data, queue=None, extra=None):
        keys = ["out{}".format(i + 1) for i in range(5)]
        if not self.keysAllIn(data.keys(), keys):
            raise Exception("Success Message data only accept keys: {}".format(keys))
        data = {key: data.get(key) for key in keys if data.get(key) is not None}
        data.update(success="true")
        return self._send(message, data, queue=queue, extra=extra)

    def sendFailureMessage(self, message, msg, queue=None, extra=None):
        if not isinstance(msg, str):
            raise Exception("Failure Message msg only accept string")
        data = {"msg": msg, "success": "false"}
        return self._send(message, data, queue=queue, extra=extra)

    def send(self, results, queue=None, extra=None):
        outputs = self.currentHandler.save(self.currentHandler.currentContext, results)
        return self.sendSuccessMessage(
            self.currentMessage, outputs, queue=queue, extra=extra
        )

    def sendError(self, msg, queue=None, extra=None):
        return self.sendFailureMessage(
            self.currentMessage, msg, queue=queue, extra=extra
        )

    def sendMissionMessage(self, message, data, queue=None, extra=None):
        keys = ["in{}".format(i + 1) for i in range(5)]
        if not self.keysAllIn(data.keys(), keys):
            raise Exception("Mission Message data only accept keys: {}".format(keys))
        return self._send(message, data, queue=queue, extra=extra)

    def retryPendingMessages(self, **kwargs):
        return mq.retryPendingMessages(
            self.options["recvQueue"],
            group=self.options["nodeGroup"],
            consumer=self.options["nodeId"],
            count=self.options["recvQueueRetryMaxCount"],
            maxTimes=self.options["recvQueueRetryMaxTimes"],
            timeout=self.options["recvQueueRetryTimeout"],
            maxlen=self.options["recvQueueMaxLength"],
            trimImmediately=self.options["recvQueueTrimImmediately"],
            **kwargs
        )

    def keysAllIn(self, keys, kset):
        return len(set(keys) - set(kset)) == 0


class Trigger(Stream):
    DEFAULT_MESSAGE = {}

    def _list(self, data):
        return data if isinstance(data, list) or isinstance(data, tuple) else [data]

    def generateMessage(self, **kwargs):
        message = {"id": self.generateRequestId()}
        message.update(self.DEFAULT_MESSAGE, **kwargs)
        return message

    def handlerCallback(self, *args, **kwargs):
        return self.streamCall(self.generateMessage(), *args, **kwargs)

    def loop(self):
        while True:
            yield

    def start(self):
        for data in self.loop():
            self.streamCall(self.generateMessage(), *self._list(data))
