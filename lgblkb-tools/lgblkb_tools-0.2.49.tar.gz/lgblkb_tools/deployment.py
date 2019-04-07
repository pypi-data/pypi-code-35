import os
from . import log_support as logsup
from abc import abstractmethod
from . import global_support as gsup
from fabric import Connection

class SshMan(object):
	
	def __init__(self,fabric_connection: Connection,remote_workdir: gsup.Folder):
		self.conn: Connection=fabric_connection
		# if isinstance(remote_workdir,str): remote_workdir=remote_projects_dir.create(
		# 	remote_workdir)
		assert isinstance(remote_workdir,
		                  gsup.Folder),f"'remote_workdir' is neither a Folder nor a string."
		self.workdir: gsup.Folder=remote_workdir
		if self.conn.run(f'[ -d "{remote_workdir.path}" ] && echo "exist" || echo "not exist"',warn=True).stdout.strip()=='not exist':
			logsup.logger.info('Creating folder %s on remote host.',remote_workdir.path)
			self.conn.run(f'mkdir -p {remote_workdir.path}')
	
	def check_exists(self,program_name):
		which_result=self.conn.run(f'which {program_name}',warn=True)
		if which_result.failed: return False
		else:
			logsup.logger.info(f'"{program_name}" already exists.')
			return True
	
	def apt_install(self,*package_names,forced=False):
		names=list()
		for package_name in package_names:
			pack_names=[x for x in package_name.split(" ") if x]
			names.extend(pack_names)
		
		if not forced:
			for package_name in names.copy():
				if self.check_exists(package_name):
					names.remove(package_name)
					logsup.logger.info('Skipping installation of "%s".',package_name)
		
		for package_name in names:
			self.run(f'sudo apt-get install {package_name} -y')
			package_path=self.conn.run(f'which {package_name}',warn=True).stdout.strip()
			logsup.logger.debug('"%s" path: %s',package_name,package_path)
	
	@abstractmethod
	def initial_setup(self,*args,**kwargs):
		pass
	
	@abstractmethod
	def execute(self,*args,**kwargs):
		pass
	
	def run(self,command,**kwargs):
		logsup.logger.info('Running !!!%s!!!',command)
		return self.conn.run(command,**kwargs)
	
	def put(self,local,remote,preserve_mode=True,absolute_remote=False):
		if not absolute_remote: remote=self.workdir.get_filepath(remote)
		
		logsup.logger.info('Putting from !!!%s!!! to !!!%s!!!',local,remote)
		return self.conn.put(local,remote=remote,preserve_mode=preserve_mode)
	
	def get(self,remote,local=None,preserve_mode=True):
		logsup.logger.info('Getting from !!!%s!!! to !!!%s!!!',remote,local)
		self.conn.get(remote,local=local,preserve_mode=preserve_mode)
	
	def cd(self,path):
		return self.conn.cd(path=path)
	
	def cd_to_working_dir(self):
		return self.cd(self.workdir.path)
	
	def prefix(self,command):
		return self.conn.prefix(command=command)
	
	def sudo(self,command,**kwargs):
		return self.conn.sudo(command=command,**kwargs)

def main():
	pass

if __name__=='__main__':
	main()
