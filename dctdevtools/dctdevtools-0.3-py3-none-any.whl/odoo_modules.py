import os
import pathlib

base_odoo_structure = ['data','models','controllers','views','static','report','wizard','test','security']

def init_module(module_name, first_model=None):
	try:
		os.mkdir(module_name)
		createFiles(module_name, ['__init__.py','__manifest__.py'])
		for current_dir in base_odoo_structure:
			dir_path = "%s/%s" % (module_name, current_dir)
			os.mkdir(dir_path)
			if 'controllers' == current_dir:
				createFiles(dir_path, ['__init__.py','main.py'])
			if 'models' == current_dir:
				createFiles(dir_path, ['__init__.py'])
				if first_model:
					createFiles(dir_path, ['%s.py'%first_model])
			if 'data' == current_dir:
				if first_model:
					createFiles(dir_path, ['%s_data.xml'%first_model])
			if 'report' == current_dir:
				createFiles(dir_path, ['__init__.py'])
				if first_model:
					createFiles(dir_path, ['%s_security.xml'%first_model])
			if 'security' == current_dir:
				createFiles(dir_path, ['ir.model.access.csv'])
			if 'views' == current_dir:
				createFiles(dir_path, ['ir.model.access.csv'])
				if first_model:
					createFiles(dir_path, ['%s_views.py'%first_model])
					createFiles(dir_path, ['%s_templates.xml'%first_model])
			if 'static' == current_dir:
				for sub_dir in ['js','css','less','xml']:
					os.mkdir("%s/%s/%s" % (module_name,current_dir,sub_dir))
		populate_init_file(module_name)
		populate_manifest(module_name)

	except OSError:
		print("Creation of the directory %s failed" % module_name)
	else:
		print("Successfully created the directory %s" % module_name)

def createFiles(folder_path, file_names):
	
	for file_name in file_names:
		# os.mknod("%s/%s"%(folder_path,file_name))
		p = open("%s/%s"%(folder_path,file_name),'w')
		p.write("")
		p.close()

def populate_init_file(file_path):
	current_dir = pathlib.Path(file_path)
	content = ""
	for d in os.listdir(current_dir):
		if os.path.isdir(os.path.join(current_dir,d)):
			for f in filter(lambda x: not os.path.isdir(os.path.join(current_dir,d,x)),os.listdir(os.path.join(current_dir,d))):
				if f == '__init__.py':
					content += "from . import %s\n" % d

	init_file = open(os.path.join(current_dir,'__init__.py'),'w')
	init_file.write(content)
	init_file.close()

def populate_manifest(file_path):
	manfifest = pathlib.Path(os.path.join(file_path,'__manifest__.py'))

	f = open(manfifest, 'w')
	f.write("{\n\
	'name': '[Module Name]',\n\
	'description': '[Description]',\n\
	'author': 'DCT Solutions',\n\
	'website': 'dctsolutions.io',\n\
	'category': 'dct_module',\n\
	'version': '0.1',\n\
	'depends':[],\n\
	'data':[\n\
		# =========================================\n\
        # DEFAUL GROUPS\n\
        # =========================================\n\n\n\
		# =========================================\n\
        # WIZARDS\n\
        # =========================================\n\n\n\
		# =========================================\n\
        # VIEWS and WEB PAGES\n\
        # =========================================\n\n\n\
		# =========================================\n\
        # STYLES\n\
        # =========================================\n\n\n\
		# =========================================\n\
        # CRONS\n\
        # =========================================\n\n\n\
		# =========================================\n\
        # MENUS\n\
        # =========================================\n\n\n\
		# =========================================\n\
        # REPORTS and CUSTOM ASSETS\n\
        # =========================================\n\n\n\
		# =========================================\n\
        # MASTER DATA\n\
        # =========================================\n\n\n\
		# =========================================\n\
        # SECURITY\n\
        # =========================================\n\n\n\
	],\n}")

	f.close()