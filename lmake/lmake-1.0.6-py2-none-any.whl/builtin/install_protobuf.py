#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Hawtian Wang (wanghaotian@agora.io)"

import re
import os
import os.path
import subprocess
import fcntl
import select
import errno
import sys

URL_BASE = "https://github.com/protocolbuffers/protobuf/releases/download/v{}/protobuf-cpp-{}.tar.gz"
FILENAME_BASE = "protobuf-cpp-{}.tar.gz"
VERSION = "3.7.0"

class bcolors:
    """
    Terminal Colors
    """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def make_async(fd):
    """
    Helper function to add the O_NONBLOCK flag to a file descriptor
    """
    fcntl.fcntl(fd, fcntl.F_SETFL, fcntl.fcntl(fd, fcntl.F_GETFL) | os.O_NONBLOCK)

def read_async(fd):
    """
    Helper function to read some data from a file descriptor, ignoring EAGAIN errors
    """
    try:
        return fd.read()
    except IOError as e:
        if e.errno != errno.EAGAIN:
            raise e
    else:
        return ''

def run_command(cmd, cwd=None, silence=False):
    """
    Run command, get stdout and stderr
    """
    print "Run command:", cmd, ", with cwd:", cwd
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd)

    make_async(process.stdout)
    make_async(process.stderr)

    stdout = []
    stderr = []
    return_code = None

    while True:
        # Wait data to become avaliable
        select.select([process.stdout, process.stderr], [], [])

        # Try reading some data from each
        stdout_piece = read_async(process.stdout)
        stderr_piece = read_async(process.stderr)

        if stdout_piece and not silence:
            print stdout_piece,
        if stderr_piece and not silence:
            print bcolors.WARNING + stderr_piece + bcolors.ENDC,

        stdout.append(stdout_piece)
        stderr.append(stderr_piece)

        return_code = process.poll()

        if return_code != None:
            if return_code != 0:
                print bcolors.FAIL + "Script error..." + bcolors.ENDC
                exit(0)
            return

def get_platform():
    return int(sys.argv[1])

def get_install_dir():
    return os.path.join(os.getcwd(), '.build', '.lib', 'm{}'.format(get_platform()))

def get_cache_dir():
    return  os.path.join(os.getcwd(), '.build', '.cache', 'm{}'.format(get_platform()))

def check_installed():
    lib_path = os.path.join(get_install_dir(), "lib",  "libprotobuf.a")
    if os.path.exists(lib_path):
        return True
    return False

def install():
    url = URL_BASE.format(VERSION, VERSION)

    print "Download protobuf from url: ", url
    cache_dir = get_cache_dir()
    install_dir = get_install_dir()

    run_command(["mkdir", "-p", cache_dir])
    run_command(["mkdir", "-p", install_dir])
    if not os.path.exists(os.path.join(cache_dir, FILENAME_BASE.format(VERSION))):
        run_command(["wget", url], cwd=cache_dir)
    run_command(["tar", "xf", FILENAME_BASE.format(VERSION)], cwd=cache_dir)

    protobuf_folder = os.path.join(cache_dir, "protobuf-{}".format(VERSION))
    platform = get_platform()
    if platform == 32:
        arg = "--host=i686-linux-gnu"
    else:
        arg = ""
    run_command(["./configure", arg,
                 "--prefix={}".format(install_dir),
                 "CFLAGS=-m{}".format(platform),
                 "CXXFLAGS=-m{}".format(platform),
                 "LDFLAGS=-m{}".format(platform),
                 ], cwd=protobuf_folder)
    run_command(["make", "-j8"], cwd=protobuf_folder)
    run_command(["make", "install"], cwd=protobuf_folder)

def main():
    if check_installed():
        print "Protobuf has installed"
        return

    install()

if __name__ == '__main__':
    main()

