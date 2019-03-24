# !/usr/bin/env python
# -*- coding: utf-8 -*-
import importlib
import pkgutil
import public


@public.add
def getmodules():
    """return a list of `task_*` module objects"""
    modules = []
    for finder, name, ispkg in pkgutil.iter_modules():
        if name.startswith('task_'):
            module = importlib.import_module(name)
            modules.append(module)
    return modules
