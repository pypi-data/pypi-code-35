# coding=utf-8
from __future__ import print_function

import contextlib
import itertools
import traceback
from collections import defaultdict

from suanpan import interfaces, objects
from suanpan.log import logger


class Arguments(objects.Context):
    pass


class Result(objects.Context):
    pass


class Component(interfaces.HasArguments):
    def __init__(self, funcOrComponent):
        if isinstance(funcOrComponent, Component):
            self.runFunc = funcOrComponent.runFunc
            self.arguments = funcOrComponent.arguments
        else:
            self.runFunc = funcOrComponent
            self.arguments = defaultdict(list)

    def __call__(self, *arg, **kwargs):
        try:
            self.run(*arg, **kwargs)
        except Exception as e:
            logger.error(traceback.format_exc())
            raise e

    @property
    def name(self):
        return self.runFunc.__name__

    def run(self, *arg, **kwargs):  # pylint: disable=unused-argument
        logger.info("Starting...")
        context = self.init()
        results = self.runFunc(context)
        self.save(context, results)
        logger.info("Done.")

    def init(self):
        restArgs = self.getArgList()
        globalArgs, restArgs = self.loadGlobalArguments(restArgs=restArgs)
        self.initBase(globalArgs)
        context = self._getContext(globalArgs)
        args, restArgs = self.loadComponentArguments(context, restArgs=restArgs)
        setattr(context, "args", args)
        return context

    def initBase(self, args):
        pass

    def save(self, context, results):
        outputs = self.saveOutputs(context, results)
        self._closeContext()
        return outputs

    @contextlib.contextmanager
    def context(self, args=None):  # pylint: disable=unused-argument
        yield objects.Context()

    def _getContext(self, *args, **kwargs):
        self.contextManager = self.context(  # pylint: disable=attribute-defined-outside-init
            *args, **kwargs
        )
        return next(self.contextManager.gen)  # pylint: disable-msg=e1101

    def _closeContext(self):
        try:
            next(self.contextManager.gen)  # pylint: disable-msg=e1101
        except StopIteration:
            pass

    def loadGlobalArguments(self, restArgs=None, **kwargs):
        logger.info("Loading Global Arguments:")
        arguments, restArgs = super(Component, self).loadGlobalArguments(
            restArgs=restArgs, **kwargs
        )
        args = {arg.key: arg.value for arg in arguments}
        return Arguments(**args), restArgs

    def loadComponentArguments(self, context, restArgs=None):
        logger.info("Loading Component Arguments:")
        _, restArgs = self.loadFormatArguments(
            context, restArgs=restArgs, exclude="outputs"
        )
        _, restArgs = self.loadCleanArguments(
            context, restArgs=restArgs, include="outputs"
        )
        arguments = {
            k: {arg.key: arg.value for arg in v if arg.isSet}
            for k, v in self.arguments.items()
        }
        arguments.update(
            {arg.key: arg.value for arg in itertools.chain(*self.arguments.values())}
        )
        return Arguments(**arguments), restArgs

    def getArguments(self, include=None, exclude=None):
        includes = set(self.arguments.keys() if not include else self._list(include))
        excludes = set([] if not exclude else self._list(exclude))
        includes = includes - excludes
        argumentsLists = [self.arguments[c] for c in includes]
        return list(itertools.chain(*argumentsLists))

    def saveMutipleOutputs(self, context, outputs, results):
        if isinstance(results, (tuple, list)):
            results = (Result(value=result) for result in results)
            return self.saveArguments(context, outputs, results)
        if isinstance(results, dict):
            outputs, results = zip(
                *[
                    (argument, Result(value=results[argument.key]))
                    for argument in outputs
                    if results.get(argument.key) is not None
                ]
            )
            return self.saveArguments(context, outputs, results)
        raise Exception("Incorrect results: {}".format(results))

    def saveOneOutput(self, context, output, results):
        result = (
            Result(value=results[output.key])
            if isinstance(results, dict) and output.key in results
            else Result(value=results)
        )
        return {output.key: output.save(context, result)}

    def saveOutputs(self, context, results):
        logger.info("Saving...")
        outputs = self.getArguments(include="outputs")
        if len(outputs) > 1:
            return self.saveMutipleOutputs(context, outputs, results)
        if len(outputs) == 1:
            return self.saveOneOutput(context, outputs[0], results)
        return None

    def addArgument(self, arg, argtype="args", reverse=True):
        if reverse:
            self.arguments[argtype].insert(0, arg)
        else:
            self.arguments[argtype].append(arg)

    @classmethod
    def arg(cls, argument, argtype="args", reverse=True):
        def _dec(funcOrComponent):
            funcOrComponent = (
                funcOrComponent
                if isinstance(funcOrComponent, cls)
                else cls(funcOrComponent)
            )
            funcOrComponent.addArgument(argument, argtype=argtype, reverse=reverse)
            return funcOrComponent

        return _dec

    @classmethod
    def input(cls, *args, **kwargs):
        kwargs.update(argtype="inputs")
        return cls.arg(*args, **kwargs)

    @classmethod
    def output(cls, *args, **kwargs):
        kwargs.update(argtype="outputs")
        return cls.arg(*args, **kwargs)

    @classmethod
    def param(cls, *args, **kwargs):
        kwargs.update(argtype="params")
        return cls.arg(*args, **kwargs)

    @classmethod
    def column(cls, *args, **kwargs):
        kwargs.update(argtype="columns")
        return cls.arg(*args, **kwargs)

    def _list(self, params=None):
        return [params] if isinstance(params, str) else list(params)
