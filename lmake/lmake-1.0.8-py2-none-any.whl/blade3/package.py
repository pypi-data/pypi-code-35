#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'liuyong@agora.io(Yong Liu)'

import os
import fnmatch
import glob
import sys
import rule_generator

from config import build_dir
from config import makefile_header
from config import settings_list

"""
a package has BUILD file to describe the build rules
including:
   cc_library: build c lib, such as libbase.a
   cc_binary: build a binary, such as http_server
   cc_lib: create a rule export exisiting lib
   cc_test: create unittest
   gen_proto: generate pb.cc and pb.h based on .proto file
"""

"""
store package including build package, deps on package,by
packageName : package
"""
globalPackages = {}
currentPackage = None

def findFiles(root_dir, file_pattern):
  matches = []
  for root, dirnames, filenames in os.walk(root_dir):
    for filename in fnmatch.filter(filenames, file_pattern):
      matches.append(os.path.join(root, filename))
  return matches


def isSourceFile(filename):
  suffices = set([ "h", "inl", "c", "cpp", "cc" ])
  ext = filename.split(".")[-1]
  return ext in suffices

def emitSingleLint(src_file, f):
  lint_file = build_dir + "/lint/" + src_file + ".lint"
  (lint_dir, filename) = os.path.split(lint_file)

  print >>f, "lint:", lint_file
  print >>f, "\n"

  print >>f, "%s: %s" %(lint_file, src_file)
  print >>f, '\t@${PRINT} "__lint check: %s"' % (src_file)

  print >>f, "\tif [ ! -x %s ]; then mkdir -p %s; fi" %(lint_dir, lint_dir)
  print >>f, "\t${CPPLINT} %s" %src_file
  print >>f, "\ttouch %s" %lint_file
  print >>f, "\n"

def loadNoLintFiles(path, filename, nolint):
  try:
    print "try to load nolint file: ", filename

    for line in file(filename, "r"):
      line = line.strip()
      for s in glob.glob(os.path.join(path, line)):
        nolint.add(s)
        print "Nolint: ", s
  except Exception, e:
    return

def emitLint(packages, f):
  nolint = set()

  skipped = "%s/nolint.txt" % os.path.dirname(os.path.realpath(__file__))
  loadNoLintFiles("", skipped, nolint)

  print >>f

  # print "Emitting lint for packages: ", packages, globalPackages
  for package in globalPackages.values():
    cc_files = []

    nolint_file = os.path.join(package.packageName, "nolint.txt")
    loadNoLintFiles(package.packageName, nolint_file, nolint)

    for a in os.walk(package.packageName):
      cc_files = cc_files + [ "/".join([a[0], b]) for b in a[2] if isSourceFile(b) ]

    # 过滤掉一些不该 lint 的源码
    cc_files = [sf for sf in cc_files
                if not sf.endswith(".gperf.cc")
                and not sf.endswith(".tab.cc")
                and not sf.endswith(".yacc.cc")
                and not sf.endswith(".lex.cc")
                and not sf.endswith(".yacc.h")
                and not sf.endswith(".lex.h")
                and not os.path.basename(sf).startswith(".")
                and not os.path.basename(sf).startswith("#")
                and sf not in nolint]

    for src_file in cc_files:
      emitSingleLint(src_file, f)

  print >>f

def generateRepoCheck(setting, f):
  repo_set = set()
  for package in globalPackages:
    repo_set.add(package.split('/')[0])

  if setting not in ("release", "static_release"):
    for repo in repo_set:
      print >>f, setting + "_" + repo + ":"
      print >>f
    return

  repo_check_program = "python -m 'lmake.blade3.repo_check' --repo"
  for repo in repo_set:
    print >>f, setting + "_" + repo + ":"
    print >>f, "\t@%s %s" %(repo_check_program, repo)
    print >>f

def emitMake(platform, extra_flags, packages, f):
  """
   1. emit BUILDFLAGS for debug and relase building
   2. create default rule depend on CTARGET argument
   3. for each rule, emit it rule and depending rule to makefile
  """
  from lmake.blade3.config import find_build_root
  try:
    for setting in settings_list:
      print >>f, "%s: lint" %setting

    print >>f, "PLATFORM =", platform
    print >>f, 'EXTRA_CXXFLAGS = %s' % extra_flags
    print >>f

    print >>f, "MEDIA_BUILD_ROOT_PATH =", os.path.dirname(os.path.dirname(__file__))
    print >>f, "%s" % file(makefile_header).read()
    print >>f
  except Exception, e:
    print >>sys.stderr, e
    sys.exit(-1)

  rules_to_build = []
  for package in packages:
    if package.isPubOnly:
      for rule in package.ruleList:
        if rule.is_unittest:
          rules_to_build.append(rule)
    else:
      for rule in package.ruleList:
         rules_to_build.append(rule)

  for rule in rules_to_build:
    rule.emitMake(f)

  print >>f

  """
   debug is the default debug binary rule,
   release is the default release rule
  """
  for settings_name in settings_list:
    generateRepoCheck(settings_name, f)

    targets_list = [ rule.makeTargetName(settings_name)
                     for rule in rules_to_build if rule.is_binary == 1 or
                     rule.is_library == 1 or rule.is_pyext == 1]

    print >>f, "%s: pre" %(settings_name)
    print >>f

    for (target) in targets_list:
      print >>f, "%s: %s" %(settings_name, target)
      print >>f

  # emit rule to run all unit tests for current packages
  all_test_target_num = 0
  for settings_name in settings_list:
    test_targets = [rule.makeTargetName(settings_name) for rule in rules_to_build
                    if rule.is_unittest == 1]
    all_test_target_num = all_test_target_num + len(test_targets)

    print >>f, "%s_test: %s %s" % (settings_name, settings_name, " ".join(test_targets))
    for test in test_targets:
      print >>f, "\t@${PRINT}"
      print >>f, "\t@${PRINT_WARNING} $$ %s ${UNIT_TEST_OPTIONS}" % test
      print >>f, "\t@%s ${UNIT_TEST_OPTIONS}" % test

    if len(test_targets) == 0:
      print >>f, "\t@${PRINT_WARNING} 'No test defined in your BUILD files'"
    print >>f

    if len(test_targets) == 0:
      print >>f, "%s_test_until_die: internal_no_test_defined" % settings_name
      print >>f
    else:
      print >>f, "%s_test_until_die: internal_%s_test_until_die" % (settings_name, settings_name)
      print >>f

  # emit rule to run all script tests for current packages
  script_files = []
  for rule in rules_to_build:
    if rule.is_script_test == 1:
      script_files.extend(rule.scriptsPathList())
  all_test_target_num = all_test_target_num + len(script_files)

  print >>f, "ss_test: %s %s" % (" ".join(settings_list), " ".join(script_files))
  for ss_test in script_files:
    print >>f, "\t@${PRINT}"
    print >>f, "\tbash -x %s" % ss_test
  if len(script_files) == 0:
    print >>f, "\t@${PRINT_WARNING} 'No shell script test defined in your BUILD files'"
  print >>f

  if all_test_target_num == 0:
    print >>f, "test_until_die: internal_no_test_defined"
    print >>f
  else:
    print >>f, "test_until_die: internal_test_until_die"
    print >>f

  # emit rule to update Makefile
  print >>f, "Makefile: %s" % " ".join([globalPackages[a].packageName + "/BUILD" for a in globalPackages])
  print >>f, "\t@${PRINT_ERROR} BUILD file updated: $?"
  print >>f, "\t@${PRINT_ERROR} Please run ./gen_makefile.sh to update the Makefile"
  print >>f, "\t@false"
  print >>f

  if not os.path.exists(".blade"):
    os.mkdir(".blade");

  # emit all deps
  p = file(".blade/all_deps", "w")
  print >>p, "packages = {"
  for package in packages:
    print >>p, "'//%s/BUILD': %s," % (package.packageName,
                                    set([("//%s/BUILD:%s" % (package.packageName, i.ruleName))
                                         for i in package.ruleList]))
  print >>p, "}"
  print >>p, "deps_graph = {"
  for name in globalPackages:
    for r in globalPackages[name].ruleList:
      print >>p, "'//%s/BUILD:%s': %s," % (name, r.ruleName,
                                         set([(i if not i.startswith(":") else "//" + name + "/BUILD" + i)
                                              for i in r.depsList]))
  print >>p, "}"
  print >>p, "rule_types = {"
  for name in globalPackages:
    for r in globalPackages[name].ruleList:
      print >>p, "'//%s/BUILD:%s': '%s'," % (name, r.ruleName, r.buildName)
  print >>p, "}"

  # emit src files
  p = file(".blade/src_files", "w")
  print >>p, "# Do NOT modify this file. It's auto-generated by gen_makefile."
  for package in packages:
    for src in findFiles(package.packageName, "*.cpp"):
      print >>p, "%s" % (src)

  # emit pub files
  p = file(".blade/files_to_pub", "w")
  print >>p, "# Do NOT modify this file. It's auto-generated by gen_makefile."
  print >>p
  print >>p

  for package in packages:
    # ignore private first
    if package.isPrivate: continue
    if package.isPubOnly: continue
    for r in package.ruleList:
      has_file_to_pub = False
      for settings_name in settings_list:
        if r.is_library:
          has_file_to_pub = True
          print >>p, "%s/%s/targets/%s/lib%s.a\tpub/%s/targets/%s" \
              % (build_dir, settings_name, package.packageName,
                 r.ruleName, settings_name, package.packageName)

      if r.is_data:
        has_file_to_pub = True
        for s in r.srcsList:
          file_path = "/".join([package.packageName, s])
          pub_file_dir = os.path.dirname("pub/src/" + file_path)
          print >>p, "%s\t%s" % (file_path, pub_file_dir)

      if r.is_shell_script:
        has_file_to_pub = True
        for s in r.srcsList:
          file_path = "/".join([package.packageName, s])
          pub_file_dir = os.path.dirname("pub/src/" + file_path)
          print >>p, "%s\t%s" % (file_path, pub_file_dir)

      if has_file_to_pub: print >>p

    for src in [package.packageName + "/BUILD"]:
      pub_dir = os.path.dirname("pub/src/" + src)
      print >>p, "%s\t%s" % (src, pub_dir)
    print >>p
    for src in findFiles(package.packageName, "*.h"):
      pub_dir = os.path.dirname("pub/src/" + src)
      print >>p, "%s\t%s" % (src, pub_dir)
    print >>p
    for src in findFiles(package.packageName, "*_test.cpp"):
      pub_dir = os.path.dirname("pub/src/" + src)
      print >>p, "%s\t%s" % (src, pub_dir)
    print >>p
    for src in findFiles(package.packageName, "*.proto"):
      pub_dir = os.path.dirname("pub/src/" + src)
      print >>p, "%s\t%s" % (src, pub_dir)
    print >>p

  print >>f

  # emit executable files
  p = file(".blade/exe_files", "w")
  print >>p, "# Do NOT modify this file. It's auto-generated by gen_makefile."
  print >>p
  print >>p
  for package in packages:
    for r in package.ruleList:
      has_file_to_pub = False
      if r.is_binary:
        for settings_name in settings_list:
          print >>p, "%s/%s/targets/%s/%s" % (build_dir, settings_name, package.packageName, r.ruleName)
    print >>p

  print >>f

  # emit lint depencies
  emitLint(packages, f)

class Package(object):
  def __init__(self, name, dirPrefix, platform):
    '''
      name is the from the root dir, such as directory:
      /
      /base/BUILD
      /net/server/BUILD
      /net/client/BUILD
      the valid package can be:base, base/, net/server, net/server/,
                               net/client, net/client/
      dirPrefix is the root dir of package, above is /
    '''
    self.buildFileName = "BUILD"
    self.platform = platform

    if name.startswith("./"):
      name = name[2:]
    if name.endswith("/"):
      name = name[:-1]

    self.packageName = name
    print "load package: //%s/BUILD" % name

    self.is_third_party = False

    self.dirPrefix = dirPrefix
    self.ruleList = []
    self.ruleMap = {}
    self.Glob = {}
    self.isPubOnly = False

    # no files should be copid to //pub, if the package is private
    self.isPrivate = False

    globalPackages[self.packageName] = self

    self.checkPackage();

  def setPrivate(self):
    self.isPrivate = True

  def checkPackage(self):
    if self.packageName.startswith("pub/"):
      print >>sys.stderr, "Can't config public only package:", self.packageName
      sys.exit(-1)
    cur = ""
    for p in self.packageName.split("/")[0:-1]:
      if cur == "":
        cur = p
      else:
        cur = cur + "/" + p
      if os.path.exists(cur + "/BUILD"):
        print >>sys.stderr, "A package's sub-dir can't contain other packages:"
        print >>sys.stderr, self.packageName + "/BUILD"
        print >>sys.stderr, cur + "/BUILD"
        sys.exit(-1)

  def dump(self):
    print "Package: //%s/BUILD%s" % (self.packageName, (" in pub" if self.isPubOnly else ""))
    if self.isPrivate:
      print "        attr: private = true"
    for rule in self.ruleList:
      rule.dump()

  def addRule(self, rule):
    if rule.ruleName not in self.ruleMap:
      self.ruleMap[rule.ruleName] = rule
      self.ruleList.append(rule)
    else:
      print "%s declares two times in BUILD" % rule.ruleName
      sys.exit(1)

  def getRule(self, ruleName):
    if ruleName not in self.ruleMap:
      return None
    return self.ruleMap[ruleName]

  @staticmethod
  def createPackage(packageName, dirPrefix, platform):
    pkg = Package(packageName, dirPrefix, platform)
    pkg.readPackage()
    return pkg

  def readPackage(self):
    """
     Read BUILD file from dirPrefix/packageName/BUILD,
     execute the build file, it will create rules in the build file
     or in dependent build files, and add them to the rulelist and rulemap
    """

    print 'Read package: ({}, {})'.format(self.packageName, self.buildFileName)
    buildFilePath = os.path.join(self.packageName, self.buildFileName)
    if not os.path.exists(buildFilePath):
      print >>sys.stderr, "BUILD file not found:", buildFilePath
      sys.exit(-1)

    packageDir = os.path.dirname(buildFilePath)

    # CHECK: a package can't be under other package's directory
    parentDir = os.path.dirname(self.packageName)
    while True:
      if os.path.isabs(self.packageName):
        pb = os.path.join(parentDir, self.buildFileName)
      else:
        pb = os.path.join(self.dirPrefix, parentDir, self.buildFileName)
      print 'Check pb:', pb
      if os.path.exists(pb):
        print >>sys.stderr, "Packages can't be nested:"
        print >>sys.stderr, pb
        print >>sys.stderr, buildFilePath
        sys.exit(-1)
      if len(parentDir) == 0: break
      parentDir = os.path.dirname(parentDir)
      if parentDir == os.path.dirname(parentDir):
        break

    executeContext = globals()
    rule_generator.insertIntoContext(executeContext)

    buildFileContent = open(buildFilePath, "r").read()
    if not buildFileContent.endswith("\n"):
      buildFileContent += "\n"

    global currentPackage

    currentPackage = self
    self.execute(buildFilePath, buildFileContent, globals(), locals())

    if len(self.ruleList) == 0:
      print >>sys.stderr, "Rules not found in BUILD file:", buildFilePath
      sys.exit(-1)

  def execute(self, filename, build, context, local):
    try:
      exec build in context, local
    except Exception, e:
      print >>sys.stderr, "failed to parse %s" % filename
      error_type = str(type(e))
      if error_type.startswith("<type 'exceptions."):
        error_type = error_type[18:]
      if error_type.endswith("'>"):
        error_type = error_type[:-2]
      print >>sys.stderr, "%s:\n%s" % (error_type, e)
      sys.exit(-1)

  def expandRules(self):
    """ expand rule and it's depending rules"""
    for rule in self.ruleList:
      rule.expandRule()

  def realPackageName(self):
    # strip prefix to get real package name
    if self.packageName.startswith("java/"):
      return self.packageName[len("java/"):]
    if self.packageName.startswith("javatest/"):
      return self.packageName[len("javatest/"):]
    if self.packageName.startswith("third_party/java/"):
      return self.packageName[len("third_party/java/"):]
    return self.packageName

  def packageRoot(self):
    return self.realPackageName().split("/")[0]

