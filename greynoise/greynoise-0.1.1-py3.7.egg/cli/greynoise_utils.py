#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Utility functions
# By hermit
import json
import os
import sys


	### CLI variables ###
class utils():
	CONFIG_PATH = os.path.expanduser('~/.config/greynoise')
	CONFIG_FILE = os.path.join(CONFIG_PATH, 'config.json')
	CONFIG_DEFAULTS = {'api_key': ''}

	def setup():
		# Called when <-k or --api-key + some argument> used.
		# TODO: key verification using ping endpoint 
		# Auto-check at some interval? Configurable?
		# If query is run w/o valid credentials, it will be unsuccessful - speaks for itself

		if len(sys.argv) >= 4 and (sys.argv[2] == "-k" or sys.argv[2] == "--api-key"):
			print(" Generating config.json...\n")
			if not os.path.isfile(utils.CONFIG_FILE):
				if not os.path.exists(utils.CONFIG_PATH):
					os.makedirs(utils.CONFIG_PATH)
				config = utils.CONFIG_DEFAULTS
				config['api_key'] = sys.argv[3] # wip
				with open(utils.CONFIG_FILE, 'w') as file:
					json.dump(config, file, indent=4, separators=(',', ': '))
					# TODO: Test if running this overwrites or appends. It needs to overwrite.
					print(" Success!\n ~/.config/greynoise/config.json file generated.\n")
					exit()
		else: # If you are w/o the above things, there's a mistake
			print(" Setup requires an API key.\n Usage: greynoise setup -k <your API key>")
			exit()


	# Parse json from config file, return api key to caller
	def load_config():
		# test for existence of file again before actually executing
		if os.path.isfile(utils.CONFIG_FILE):
			config = json.load(open(utils.CONFIG_FILE))
			if "api_key" in config:
				# print(config['api_key'])
				return config['api_key']#.encode('utf-8')
			else:
				return ''
				print(" API key not found.\n")
				exit()

	# Turns input file into a python list
	def listFile(listFile):
		try:
			with open(listFile) as f:
				ipList = []
				inputFile = f.readlines()
				for i in inputFile: 
					i = i.split("\n")[0]
					ipList.append(i)
			return ipList
		except:
			return None
	 
	# TODO: write set_defaults, load_defaults
	# Configure what greynoise does by default, ie, when greynoise <query> is run.
	# in this case, use_defaults? (outFormat = defaultFormat, etc)
	  # Implement this function in utils.py 
	# add these to config.json - user can modify it directly
	# Doing it by command line could be tedious, but could be good to provide for convenience.
	# Ways to do it:
	    # Ask user to provide (key,value) for settings they want to overwrite, -1 to quit
	    # greynoise setup -d/--defaults
	        # if this is entered, call set_defaults()
	        # list defaults that can be set (numbered)
	        # print current default value in parentheses next to each
	        # user provides name or number of the variable they wanna set. (if it's valid,)
	        # user is prompted for the value they want to give to that variable. (if it's valid,)
	        # add to a dict of defaults that were changed.
	        # for each in changed defaults, find the same key in config.json, and give it the new value
	        # call update_defaults()
	        # TODO: Update value of default variables by loading config.json
	        # update_defaults() should also be called by setup() whenever it is run 


	        # set value locally, as well as open+write value to config file, then repeat loop:
	        # list of the default variables and their current values prints again (-1 to quit)

	        # when prompted to pick a number for a variable, user could also just provide number,value
	        # and skip right to testing the validity of both. either option should be available.
