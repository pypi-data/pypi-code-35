#	Copyright (C) 2019, Mentice AB
#	See accompanying LICENSE file

import os
import shlex
import jsonmerge
import yaml

default_config = {
	'verbose' : False,
	'host' : '',
	'registry' : '',
	'runtime' : 'nvidia',	# Docker runtime
	'inputs' : [],
	'out' : None,
	'timeout': None,		# In seconds (None means wait indefinitely)
	'result-image': 'always' # Create a latest-result image based on container exit status: 'success', 'always', 'none' -or- 'never'
}

append_schema = {
	'properties': {
		'inputs': {
			'mergeStrategy': 'append'
		},
		'Xdocker': {
			'mergeStrategy': 'append'
		}
	}
}
merge_append_strat = jsonmerge.Merger(append_schema)

def merge_config_file(config, path):
	if os.path.isfile(path):
		with open(path, 'r') as inf:
			dict = yaml.load(inf, Loader=yaml.FullLoader)
			if dict == None: dict = {}
			config = jsonmerge.merge(config, dict)	# Note: using default merge strategy here
	return config

def find_on_path(dir, filename):
	"""Look for filename searching up through all directories on the path 'dir'.
		
	Returns the full path if the file exists, or False
	"""

	for _ in range(20):
		path = os.path.join(dir, filename)
		# print('dir',dir, 'path', path)
		if os.path.isfile(path):
			return path
		dir, _ = os.path.split(dir)
		if dir == '/': break
	return False

def get_config(config_names=['default']):
	config = merge_config_file(default_config, '~/.config/jobber/jobber-config.yml')
	config = merge_config_file(config, find_on_path(os.getcwd(), 'jobber-config.yml'))

	# Translate items if necessary (modifies the config dict in place)
	def visit(dic):
		for key, val in dic.items():
			yield dic, key, val
			if type(val) is dict:
				for dic2, key2, val2 in visit(val):
					yield dic2, key2, val2
	for dic, key, val in visit(config):
		if key in ('Xdocker', 'cmd') and type(val) is str:
			dic[key] = shlex.split(val)
		if key in ('cmd', 'timeout') and type(val) is str and val.lower() == 'none':
			dic[key] = None
	
	if 'configs' in config:
		configs = config['configs']
		config_names = list(config_names)		# make a copy
		for name in config_names:
			if name in configs:
				val = configs[name]
				if type(val) is list:
					for nm in val:
						if nm not in config_names:
							config_names.append(nm)
				else:
					config = merge_append_strat.merge(config, val)
			else:
				print('warning: config not found: {0}'.format(name))
		del config['configs']	# Remove 'configs' since they're used to populate the config dict itself

	# for k, v in config.items():
	# 	print(f'{k:16} {v}')

	return config