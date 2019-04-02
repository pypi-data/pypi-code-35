# -*- coding:utf-8 -*-

import tornado.web
from log import *
import opt
import sys
import tools


opt.add_option(	"-g", "--get",
		action="store_true", 
        dest="get", default=True, 
		help="Whether to support get methord") 

class FileHandler(tornado.web.RequestHandler):
	def get(self):  
		path = self.request.path
		if path.startswith('/'):
			path = path[1:]
		
		localpath = os.path.join('html', path+'.html')
		html = open(localpath).read()
		self.write(html)

class BaseHandler(tornado.web.RequestHandler):  
	
	def save_file(self, path, name):
		paths = []
		for k, v in self.request.files.items():
			print k, v[0].filename
			
			filename = v[0].filename
			filename = tools.transcode(filename)
			suffix = tools.get_suffix(filename)

			
			full_path = os.path.join(path, str('%s%s' % (name, suffix)))

			logger().info('save file %s', full_path)
		    	with open(full_path,'wb') as up: 
				up.write(v[0]['body'])
			up.close()
			paths.append(full_path)
		return paths

	def process(self):
		logger().error('not implement')
		sys.exit(-1)

	def get(self):  
		if opt.option().get:
			return self.process()
		else:
			msg = 'get method not supported'
			logger().error(msg)
			self.write(msg)
			
	def post(self):  
		return self.process()

	def get_arg(self, key):
		return self.get_argument(key).encode('utf-8')

	def has_arg(self, key):
		args = self.request.arguments
		return key in args

	def get_arg_ex(self, key, dft):
		if self.has_arg(key):
			return self.get_argument(key).encode('utf-8')
		else:
			return dft

def main():
	pass

if __name__ == '__main__':
	main()
