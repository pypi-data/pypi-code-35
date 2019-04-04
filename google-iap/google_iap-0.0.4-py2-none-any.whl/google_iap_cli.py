#!/usr/bin/env python

from gcpiap import GcpIap
from docopt import docopt
from signal import signal, SIGINT
from utils import signal_handler
signal(SIGINT, signal_handler)
import sys, os

usage = """
Usage:
  {0} projects list --credentials=<s>
  {0} zones list --credentials=<s> --project=<p>
  {0} instances list --credentials=<s> --project=<p> [--zone=<z>]
  {0} iap get --credentials=<s> --project=<p> [--zone=<z>] [--instance=<i>] [--format=<f>]
  {0} iap set --credentials=<s> --project=<p> [--zone=<z>] [--instance=<i>] --policy=<p>

Options:
  -h --help          Show this screen.
  --credentials=<s>  Service account json file
  --project=<p>      Project Id
  --zone=<z>         Zone name
  --instance=<i>     Instance name
  --policy=<p>       Policy json file or yaml file
  --format=<f>       Format (valid format : yaml or json) [default: yaml]
""".format('google-iap')

arguments = docopt(usage, version='0.0.4')

if 'projects' in arguments:
    if arguments['projects'] == 1: 
        if 'list' in arguments:
            if arguments['list']:
                try:
                    gcpiap = GcpIap(arguments['--credentials'])
                    for project in gcpiap.listProjects():
                        print(project)
                    sys.exit(0)
                except Exception as e:
                    print(str(e))
                    sys.exit(1)

if 'zones' in arguments:
    if arguments['zones'] == 1: 
        if 'list' in arguments:
            if arguments['list']:
                try:
                    gcpiap = GcpIap(arguments['--credentials'])
                    for zone in gcpiap.listZonesUsed(arguments['--project']):
                        print(zone)
                    sys.exit(0)
                except Exception as e:
                    print(str(e))
                    sys.exit(1)

if 'instances' in arguments:
    if arguments['instances'] == 1: 
        if 'list' in arguments:
            if arguments['list']:
                try:
                    gcpiap = GcpIap(arguments['--credentials'])
                    if not arguments['--zone'] and arguments['--project']:
                        for instance in gcpiap.listInstances(arguments['--project']):
                            print(instance)
                    elif arguments['--zone'] and arguments['--project']:
                        for instance in gcpiap.listInstancesByZone(arguments['--project'], zone=arguments['--zone']):
                            print(instance)
                    sys.exit(0)
                except Exception as e:
                    print(str(e))
                    sys.exit(1)

if 'iap' in arguments:
    if arguments['iap'] == 1: 
        if 'get' in arguments:
            if arguments['get']:
                try:
                    gcpiap = GcpIap(arguments['--credentials'])
                    if not arguments['--instance'] and not arguments['--zone'] and arguments['--project']:
                        print(gcpiap.getIapPolicy(arguments['--project'], format=arguments['--format']))
                    elif not arguments['--instance'] and arguments['--zone'] and arguments['--project']:
                        print(gcpiap.getIapPolicy(arguments['--project'], zone=arguments['--zone'], format=arguments['--format']))
                    elif arguments['--instance'] and arguments['--zone'] and arguments['--project']:
                        print(gcpiap.getIapPolicy(arguments['--project'], zone=arguments['--zone'], instance=arguments['--instance'], format=arguments['--format']))
                    sys.exit(0)
                except Exception as e:
                    print(str(e))
                    sys.exit(1)

if 'iap' in arguments:
    if arguments['iap'] == 1: 
        if 'set' in arguments:
            if arguments['set']:
                try:
                    gcpiap = GcpIap(arguments['--credentials'])
                    if not arguments['--instance'] and not arguments['--zone'] and arguments['--project']:
                        print(gcpiap.setIapPolicy(arguments['--project'], arguments['--policy']))
                    elif not arguments['--instance'] and arguments['--zone'] and arguments['--project']:
                        print(gcpiap.setIapPolicy(arguments['--project'], arguments['--policy'], zone=arguments['--zone']))
                    elif arguments['--instance'] and arguments['--zone'] and arguments['--project']:
                        print(gcpiap.setIapPolicy(arguments['--project'], arguments['--policy'], zone=arguments['--zone'], instance=arguments['--instance']))
                    sys.exit(0)
                except Exception as e:
                    print(str(e))
                    sys.exit(1)


