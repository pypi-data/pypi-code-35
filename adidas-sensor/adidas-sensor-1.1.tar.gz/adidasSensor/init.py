#!python3

__author__ = 'Dipl.-Ing. Peter Blank'

import subprocess
import sys

script			= 'tool.py'
accRange		= '16'
gyroRate		= '2000'
samplingRate	= '250'
port			= sys.argv[1]
id				= sys.argv[2]

subprocess.call('py -3 ' + script + ' ' + port + ' -ef')
subprocess.call('py -3 ' + script + ' ' + port + ' -ee')
subprocess.call('py -3 ' + script + ' ' + port + ' -r')
subprocess.call('py -3 ' + script + ' ' + port + ' -c')
subprocess.call('py -3 ' + script + ' ' + port + ' -ua ' + accRange)
subprocess.call('py -3 ' + script + ' ' + port + ' -ug ' + gyroRate)
subprocess.call('py -3 ' + script + ' ' + port + ' -id ' + id)
subprocess.call('py -3 ' + script + ' ' + port + ' -us ' + samplingRate)
subprocess.call('py -3 ' + script + ' ' + port + ' -ut')
subprocess.call('py -3 ' + script + ' ' + port + ' -ud')
subprocess.call('py -3 ' + script + ' ' + port + ' -c')
subprocess.call('py -3 ' + script + ' ' + port + ' -u')

sys.exit(0)