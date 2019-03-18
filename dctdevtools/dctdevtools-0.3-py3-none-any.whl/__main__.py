import sys
from dctdevtools import odoo_modules

def run():
	args = sys.argv[1:]

	action = args[0]
	params = args[1:]

	if 'init_odoo_module' == action:
		module_name = params[0]
		odoo_modules.init_module(module_name, params[1])
		

