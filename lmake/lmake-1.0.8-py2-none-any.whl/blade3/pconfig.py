#!/usr/bin/env python
__author__ = 'liuyong@agora.io(Yong Liu)'

import argparse

import package as p
import rule
import sys
import os
import argparse
import config
import platform

def parseArguments(argv):
  parser = argparse.ArgumentParser(description='Config Parser')
  parser.add_argument('files', metavar='N', type=str, nargs='+',
                      help='Build Files')
  target = platform.machine()
  if target in ("i386", "i686"):
    target = 32
  else:
    target = 64

  parser.add_argument('--machine', dest='target', type=int, default=target,
                      choices=(32, 64), help='Specify the platform: 32/64')

  parser.add_argument('-m', dest='target', type=int, choices=(32, 64),
                      default=target, help='Specify the platform: 32/64')

  parser.add_argument('-e', dest='extra_flags', type=str, default="",
                      help='Extra flags for all sources')
  parser.add_argument('--extra-flags', dest='extra_flags', type=str, default='',
                      help='Extra flags for all sources')

  print argv
  args = parser.parse_args(argv[1:])
  return (args.target, args.files, args.extra_flags)

def main(argv):
  (target, files, extra_flags) = parseArguments(argv)

  package_set = set()
  for packageName in files:
    packageName = packageName.strip()
    if packageName.startswith("/") or packageName.startswith("../"):
      print >> sys.stderr, "Invalid BUILD file, not a relative path: ", \
          packageName
      sys.exit(-1)

    if packageName.startswith("./"): packageName = packageName[2:]

    if not packageName.endswith("/BUILD"):
      print >> sys.stderr, "not a BUILD file: ", packageName
      print >> sys.stderr, "please specify a path to a BUILD file"
      sys.exit(-1)

    if packageName in package_set:
      print >> sys.stderr, "repeated BUILD file: " + packageName
      sys.exit(-1)
    package_set.add(packageName)

  dirPrefix = os.getcwd()
  packages = []

  for packageName in files:
    packageName = packageName.strip()
    if packageName.startswith("./"): packageName = packageName[2:]
    if not packageName.endswith("/BUILD"):
      print >> sys.stderr, "not a BUILD file: ", packageName
      print >> sys.stderr, "please specify a path to a BUILD file"
      sys.exit(-1)

    packageName = packageName[:-6]
    package = p.Package(packageName, dirPrefix, target)

    print "_____gen_makefile %s" % package.packageName

    package.readPackage()
    package.expandRules()
    packages.append(package)

  for package in p.globalPackages.values():
    package.dump()

  makeFile = open("Makefile", "w")
  p.emitMake(target, extra_flags, packages, makeFile)

if __name__ == "__main__":
  if len(sys.argv) == 1:
    print >>sys.stderr, "Please specify a package directory"
  main(sys.argv)
