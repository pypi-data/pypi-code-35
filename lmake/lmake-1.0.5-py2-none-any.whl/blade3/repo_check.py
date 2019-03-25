#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'liuyong@agora.io(Yong Liu)'

import argparse
import subprocess
import sys

def checkRepo(repo):
  git_status = subprocess.Popen(["git", "status", "-s", "--porcelain"],
                                cwd=repo, stdout=subprocess.PIPE)
  print "checking git repo:", repo
  untracked = 0
  for line in git_status.stdout:
    untracked += 1
  if untracked != 0:
    print "You have untracked/modified files to commit in git repo:", repo
    sys.exit(-1)

  git_tag = subprocess.Popen(["git", "describe", "--tags", "--exact-match"],
                             cwd=repo, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
  for line in git_tag.stderr:
    print line,

  git_tag.wait()
  if git_tag.returncode != 0:
    print "You should add a tag for the current commit before releasing in repo:", repo
    sys.exit(-1)

def main():
  parser = argparse.ArgumentParser(description='Repo status checker')
  parser.add_argument("--repo", dest="repo", default=".")
  args = parser.parse_args()
  checkRepo(args.repo)

if __name__ == "__main__":
  main()
