#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'liuyong@agora.io(Yong Liu)'


import os
import package
import rule
import cc
import sys


class ShellScript(rule.Rule):
  """
    shell_script(name = "",
                 script = [""],
                 export = "",
                 export_bin = {"name": "path"}
    )
  """
  buildName = "shell_script"

  def __init__(self, **kwargs):
    if "name" not in kwargs:
      print >> sys.stderr, "Must have a 'name' argument, see %s/BUILD " \
          "for details" % package.currentPackage.packageName
      sys.exit(-1)

    if "script" not in kwargs:
      print >> sys.stderr, "Must have a 'script' argument for //%s/BUILD:%s" \
          %(package.currentPackage.packageName, kwargs["name"])
      sys.exit(-1)

    if 'export' not in kwargs:
      print >> sys.stderr, "Must have a 'export' argument for //%s/BUILD:%s" \
          %(package.currentPackage.packageName, kwargs["name"])
      sys.exit(-1)

    rule.Rule.__init__(self, kwargs['name'], package.currentPackage)

    self.is_library = 0
    self.is_shell_script = 1
    self.script = kwargs["script"]
    self.emitted = False
    self.package.addRule(self)
    self.srcsList = [self.script]
    self.depPBHeaderPathSet = lambda: set()
    self.export = kwargs['export']
    self.exportBin = kwargs.get('export_bin', dict())

    if "deps" in kwargs:
      self.depsList = kwargs["deps"]
    else:
      self.depsList = []
    self.depRulesList = []
    self.checkArguments("deps", self.depsList)

  def checkArguments(self, name, value):
    res = True
    if type(value) != type([]):
      res = False
    if res:
      for a in value:
        if type(a) != type(""):
          res = False
    if not res:
      print "The parameter '%s' of //%s/BUILD:%s must be a list of strings" \
          % (name, self.package.packageName, self.ruleName)
      sys.exit(-1)

  def exportLibPathList(self, settings_name):
    return [self.exportFilePath()]

  def exportFilePath(self):
    return '.build/.lib/m${PLATFORM}/lib/%s' % self.export

  def exportLibDirList(self, settings_name):
    return []

  def exportLibNameList(self):
    return []

  def exportAllLibPathList(self, settings_name):
    return []

  def emitDependencies(self, f):
    for dep in self.depRulesList:
      dep.emitDependencies(f)

  def dump(self):
    print "\tshell_script: ", self.ruleName
    for f in self.srcsList:
      print "\t\tfile: ", f

  def emitMake(self, f):
    if self.emitted:
      return

    self.emitSelfMake(f)
    for dep in self.depRulesList:
      dep.emitMake(f)

    self.emitted = True

  def emitSelfMake(self, f):
    script_path = os.path.join(self.package.packageName, self.script)

    for exports in self.exportBin:
      print >>f, "%s = %s" % (exports, self.exportBin[exports])
    print >>f, "\n"

    for exports in self.exportBin:
      print >>f, "${%s}: %s" % (exports, self.exportFilePath())
      print >>f, "\n"

    print >>f, "%s:" % (self.exportFilePath())
    print >>f, '\t@${PRINT} "_____exec [%s]"' % self.ruleName
    print >>f, "\t%s ${PLATFORM}" % script_path
    print >>f, "\n"

  def makeTargetName(self):
    return os.path.join("shell", self.package.packageName, self.ruleName)

# shell script test case
# 脚本编写的测试文件，只有在所有版本的二进制 (dbg/opt/diag_dbg/diag_opt) 编译成功后，才会运行
class SSTest(cc.CCLibrary):
  """
    ss_test(name = "",
            srcs = [""]
           )
  """
  buildName = "ss_test"

  def __init__(self, **kwargs):
    cc.CCLibrary.__init__(self, **kwargs)
    self.is_library = 0
    self.is_shell_script = 1
    self.is_script_test = 1

    for src in self.srcList:
      if not src.endswith("_test.sh"):
        print >> sys.stderr, "file name of shell script test must ended with '_test.sh': %s" % src
        sys.exit(-1)

  def exportLibPathList(self, settings_name):
    return []

  def exportLibDirList(self, settings_name):
    return []

  def exportLibNameList(self):
    return []

  def scriptsPathList(self):
    return [("%s/%s" % (self.package.packageName, filename)) for filename in self.srcsList]

  def dump(self):
    print "\tss_test: ", self.ruleName
    for f in self.srcsList:
      print "\t\tfile: ", f

  def emitMake(self, f):
    pass

