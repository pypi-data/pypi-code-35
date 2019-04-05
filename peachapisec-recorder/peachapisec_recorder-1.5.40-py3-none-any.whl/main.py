
from __future__ import print_function

'''
Copyright 2017 Peach Tech

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

try:
	import click
	import mitmproxy.tools.main
	from mitmproxy.tools import dump
	from mitmproxy.tools import cmdline
	from mitmproxy import ctx
except:
	print("Error, missing dependencies.")
	print("Use 'pip install -r requirements.txt'")
	exit(-1)

import sys
from typing import Dict, List
import os
import signal
import pkg_resources
import atexit
import tempfile
import multiprocessing as mp
import time

# ################################################################################

_pidfile:str = os.path.join(tempfile.gettempdir(),"peachrunner.pid")

def addflag(args:List[str], flag:str, value:bool):
	if not value:
		return

	args.append(flag)

def addarg(args:List[str], arg:str, value:str):
	if not value:
		return

	args.append(arg)
	args.append(value)

def getpidfile(pidfile:str):
	global _pidfile

	if pidfile:
		_pidfile = pidfile

	return _pidfile

def delpid(pidfile:str):

	global _pidfile

	if pidfile:
		_pidfile = pidfile

	pid:str = str(os.getpid())

	if os.path.isfile(_pidfile):
		os.unlink(_pidfile)

def writepid(pidfile:str):

	global _pidfile

	if pidfile:
		_pidfile = pidfile

	pid:str = str(os.getpid())

	if os.path.isfile(_pidfile):
		os.unlink(_pidfile)

	with open(_pidfile, 'w') as fd:
		fd.write(pid)


def runproxy(args:List[str], foreground:bool, pid_file:str):

	if not foreground:
		if os.fork() > 0:
			return

	writepid(pid_file)

	m = mitmproxy.tools.main.run(dump.DumpMaster, cmdline.mitmdump, args, None)
	if foreground and m and m.errorcheck.has_errored:
		sys.exit(1)


# ################################################################################
# ################################################################################
# ################################################################################

@click.group(
	context_settings=dict(help_option_names=['-h', '--help']),
	help="Run one or more commands that generate traffic through Peach API Security.")
def cli():
	pass

@cli.command(help="Start recording")
@click.option('-o', '--output-file', required=True, help="Filename to record traffic to")
@click.option('-f', '--foreground', is_flag=True, default=False, help="Stay in foreground (don't fork)")
@click.option('-q', '--quiet', is_flag=True, default=False, help="Quiet")
@click.option('-v', '--verbose', is_flag=True, default=False, help="Increase output verbosity")
@click.option('-m', '--mode', default=None, help='Mode can be "regular", "transparent", "socks5", "reverse:SPEC", or "upstream:SPEC". For reverse and upstream proxy modes, SPEC is host specification in the form of "http[s]://host[:port]".')
@click.option('--anticache/--noanticache', default=False, help="Strip out request headers that might cause the server to return 304-not-modified.")

@click.option('--listen-host', default=None, help="Address tp bind recorder to")
@click.option('-p', '--listen-port', default=None, help="Proxy service port")
@click.option('--ignore-hosts', default=None, help='Ignore host and forward all traffic without processing it. In transparent mode, it is recommended to use an IP address (range), not the hostname. In regular mode, only SSL traffic is ignored and the hostname should be used. The supplied value is interpreted as a regular expression and matched on the ip or the hostname. May be passed multiple times.')
@click.option('--tcp-hosts', default=None, help='Generic TCP SSL proxy mode for all hosts that match the pattern. Similar to --ignore, but SSL connections are intercepted. The communication contents are printed to the log in verbose mode. May be passed multiple times.')

@click.option('--certs', default=None, help='SSL certificates of the form "[domain=]path". The domain may include a wildcard, and is equal to "*" if not specified. The file at path is   certificate in PEM format. If a private key is included in the PEM, it is used, else the default key in the conf dir is used. The PEM file should contain the full certificate chain, with the leaf certificate as the first entry. May be passed multiple times.')
@click.option('--pid-file', default=None, help='Write the PID to this file.  Defaults to system temp folder + peachrunner.pid.  /tmp/peachrunner.pid on Linux')
def start(output_file:str, foreground:bool, quiet:bool, verbose:bool, mode:str, anticache:bool, listen_host:str, listen_port:str, ignore_hosts:str, tcp_hosts:str, certs:str, pid_file:str):
	"""This command starts an HTTP/HTTPS proxy to record web traffic.  The
	traffic is saved in the HAR format, suitable for use with peachrunner.
	"""

	har_dump_filename:str = pkg_resources.resource_filename(
		__name__, "har_dump.py")

	if not quiet:
		print("")
		print("]] Peach API Security: Traffic Recorder")
		print("]] Copyright (c) Peach Tech")
		print("")

	if foreground == False and sys.platform == "win32":
		print("Error, background operation not supported on Windows")
		print("Please use the '-f' or '--foreground' parameter.")
		print("")
		print("On windows, the 'start /b COMMAND' syntax can be used")
		print("to background recorder:")
		print("")
		print("  start /b peachrecorder -f -q")
		print("")
		sys.exit(1)

	extra = None
	args:List[str] = [
		'--no-http2',
		'--ssl-insecure',
		'-s', har_dump_filename,
		'--set', ('hardump=%s'% output_file),
	]

	addflag(args, '-q', quiet or not foreground)
	addflag(args, '-v', verbose)

	addarg(args, '-m', mode)

	addflag(args, '--anticache', anticache)
	addflag(args, '--no-anticache', not anticache)

	addarg(args, '--listen-host', listen_host)
	addarg(args, '-p', listen_port)
	addarg(args, '--ignore-hosts', ignore_hosts)
	addarg(args, '--tcp-hosts', tcp_hosts)
	addarg(args, '--certs', certs)

	try:
		delpid(pid_file)
	except:
		print("Error, pid file '%s' exists and deleting failed."%pid_file)

	if not foreground:
		print("Starting background recorder\n")

		p = mp.Process(target=runproxy, args=(args,foreground,pid_file))
		p.daemon = True
		p.start()
		p.join()
		time.sleep(2)

	else:
		runproxy(args, foreground, pid_file)


@cli.command(help="Stop recording")
@click.option('--pid-file', default=None, help='Provide file with recorder PID to stop.  Defaults to TMP/peachrunner.pid')
@click.option('-q', '--quiet', is_flag=True, default=False, help="Quiet")
def stop(pid_file:str, quiet:bool):
	"""This command stops an already running recorder instance using its PID file.
	"""

	if not quiet:
		print("")
		print("]] Peach API Security: Traffic Recorder")
		print("]] Copyright (c) Peach Tech")
		print("")

	global _pidfile

	if not pid_file:
		pid_file = _pidfile

	if not os.path.exists(pid_file):
		if not quiet:
			print("Error, pid file '%s' does not exist." % pid_file)

		return 1

	with open(pid_file, "rb") as fd:
		pid :int = int(fd.read())

	if not quiet:
		print("Stopping recordering process %d" % pid)

	try:
		os.kill(pid, signal.SIGTERM)
	except OSError:
		if not quiet:
			print("Error, pid %d does not exist, or we do not have permission to terminate" % pid)
		
		sys.exit(1)


def run():
	cli(obj={}, auto_envvar_prefix='PEACH')


# end
