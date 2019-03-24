#!/usr/bin/env python
# -*- coding: utf-8 -*-
import inspect
import os
import ruamel.yaml as yaml
from ruamel.yaml.scalarstring import DoubleQuotedScalarString, SingleQuotedScalarString
import public
import replace
try:
    from stringio import StringIO
except ImportError:
    from io import StringIO

KEYS = [
    # https://docs.travis-ci.com/user/languages/
    "language",

    # https://docs.travis-ci.com/user/languages/
    # https://docs.travis-ci.com/user/languages/c/
    "compiler",

    # C#, F, Visual Basic
    # https://docs.travis-ci.com/user/languages/csharp/
    "solution",
    "mono",

    # https://docs.travis-ci.com/user/languages/cpp/
    "compiler",

    # https://docs.travis-ci.com/user/languages/clojure/
    "lein",

    # https://docs.travis-ci.com/user/languages/crystal/
    "crystal",

    # https://docs.travis-ci.com/user/languages/d/
    "d",

    # https://docs.travis-ci.com/user/languages/dart/
    "dart",
    "dart_task",
    "dartanalyzer",

    # https://docs.travis-ci.com/user/languages/erlang/
    "otp_release",

    # https://docs.travis-ci.com/user/languages/elixir/
    "elixir",
    "otp_release",

    # https://docs.travis-ci.com/user/languages/go/
    "go",
    "go_import_path",
    "gobuild_args",

    # https://docs.travis-ci.com/user/languages/groovy/
    "jdk",

    # https://docs.travis-ci.com/user/languages/haskell/
    "ghc",

    # https://docs.travis-ci.com/user/languages/haxe/
    "haxe",
    "neko",
    "hxml",

    # https://docs.travis-ci.com/user/languages/java/
    "jdk",

    # https://docs.travis-ci.com/user/languages/javascript-with-nodejs/
    "node_js",

    # https://docs.travis-ci.com/user/languages/julia/
    "julia",

    # https://docs.travis-ci.com/user/languages/nix/

    # Objective-C or Swift
    # https://docs.travis-ci.com/user/languages/objective-c/
    "osx_image",
    "xcode_project",
    "xcode_scheme",
    "xcode_sdk",
    "podfile",

    # https://docs.travis-ci.com/user/languages/perl/
    "perl",

    # https://docs.travis-ci.com/user/languages/perl6/
    "perl6",

    # https://docs.travis-ci.com/user/languages/php/
    "php",

    # https://docs.travis-ci.com/user/languages/python/
    "python",
    "virtualenv",

    # https://docs.travis-ci.com/user/languages/r/
    "r",
    "pandoc_version",
    "repos",
    "r_github_packages",
    "Imports",
    "Remotes",

    # https://docs.travis-ci.com/user/languages/ruby/
    "rvm",
    "gemfile",
    "bundler_args",
    "jdk",

    # https://docs.travis-ci.com/user/languages/rust/
    "rust",

    # https://docs.travis-ci.com/user/languages/scala/
    "scala",
    "sbt_args",

    # https://docs.travis-ci.com/user/languages/smalltalk/
    "smalltalk_vm",
    "smalltalk",

    "os",               # https://docs.travis-ci.com/user/multi-os/
    "sudo",             # https://docs.travis-ci.com/user/reference/trusty/
    "dist",             # https://docs.travis-ci.com/user/reference/trusty/
    "addons",           # https://docs.travis-ci.com/user/addons/
    "cache",            # https://docs.travis-ci.com/user/caching
    "podfile",          # https://docs.travis-ci.com/user/caching#Determining-the-Podfile-path
    "branches",         # https://docs.travis-ci.com/user/customizing-the-build/#Safelisting-or-blocklisting-branches
    "git",              # https://docs.travis-ci.com/user/customizing-the-build/#Git-Clone-Depth
    "env",              # https://docs.travis-ci.com/user/environment-variables/
    "notifications",    # https://docs.travis-ci.com/user/notifications/
    "matrix",           # https://docs.travis-ci.com/user/customizing-the-build/#Build-Matrix
    "services",         # https://docs.travis-ci.com/user/database-setup/#Starting-Services

    "after_success",
    "after_failure",
    "before_install",
    "install",
    "before_script",
    "script"
]


@public.add
def load(path=".travis.yml"):
    """return a dictonary with `.travis.yml` data"""
    if not path:
        path = ".travis.yml"
    with open(path, 'r') as stream:
        return yaml.load(stream)


@public.add
def dump(data):
    """dump a dictionary to a YAML document string"""
    stream = StringIO()
    yaml.dump(data, stream, Dumper=yaml.RoundTripDumper)
    return stream.getvalue().rstrip()


@public.add
def save(data, path=".travis.yml"):
    """save a dictionary to a file"""
    if not path:
        path = ".travis.yml"
    with open(path, 'w') as outfile:
        yaml.dump(data, outfile, Dumper=yaml.RoundTripDumper)


@public.add
def quote(value):
    """return a double quoted string"""
    return DoubleQuotedScalarString(value)


@public.add
class Classifiers:
    """python classifiers class"""
    classifiers = []

    def __init__(self):
        if os.path.exists("setup.py"):
            self.init()

    def init(self):
        self.classifiers = os.popen("python setup.py --classifiers").read().splitlines()

    def load(self, path=None):
        """load classifiers from a file"""
        if not path:
            path = "classifiers.txt"
        self.classifiers = list(filter(None, open(path).read().splitlines()))

    @property
    def language(self):
        if self.python:
            return "python"

    @property
    def pyversions(self):
        """return a list of python versions"""
        classifiers = list(filter(lambda l: "Python ::" in l, self.classifiers))
        pyversions = list(map(lambda l: l.split(" :: ")[-1], classifiers))
        return list(map(float, filter(lambda l: l.replace('.', '').isdigit(), pyversions)))

    def __str__(self):
        return "\n".join(self.classifiers)


@public.add
class Travis:
    """`.travis.yml` generator class"""
    keys = KEYS
    language = "python"
    generator_url = "https://pypi.org/project/travis-generator/"

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def python(self):
        if os.path.exists("setup.py"):
            pyversions = Classifiers().pyversions
            pyversions = replace.replace(pyversions, {3.7: "3.7-dev", 3.8: "3.7-dev"})
            for r in [2, 3]:
                if r in pyversions:
                    pyversions.remove(r)
            if pyversions:
                return list(map(quote, pyversions))
            return [quote("3.6")]

    @property
    def data(self):
        data = dict()
        for key in self.keys:
            value = getattr(self, key, None)
            if inspect.isroutine(value):
                value = value()
            if value is not None and value != "" and value != []:
                data[key] = value
        return data

    def dump(self):
        string = dump(self.data)
        if self.generator_url:
            string = "# %s\n%s" % (self.generator_url, string)
        return string

    def save(self, path=None):
        if not path:
            path = ".travis.yml"
        dirname = os.path.dirname(path)
        if dirname and not os.path.exists(dirname):
            os.makedirs(dirname)
        open(path, "w").write(str(self))

    def __str__(self):
        return self.dump()

    def __repr__(self):
        return self.dump()
