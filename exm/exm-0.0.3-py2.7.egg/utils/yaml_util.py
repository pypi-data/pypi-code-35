# coding=utf-8
import re
import os

import yaml

import expression


def load(file):
    conf = {}
    with open(file, "r") as input:
        conf = yaml.load(input)
        pass
    systemenv = dict(os.environ)
    env = {}
    env.update(systemenv)
    env.update(conf)
    env["system"] = systemenv
    conf["system"] = systemenv
    expression.evaluate(env, conf)
    return conf

