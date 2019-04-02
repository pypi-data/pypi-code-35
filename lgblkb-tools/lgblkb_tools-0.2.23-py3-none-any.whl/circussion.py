import circus
import signal

class TheWatcher(object):
	watchers=list()
	
	def __init__(self,name,cmd,numprocesses=1,warmup_delay=0.,working_dir=None,shell=True,shell_args=None,uid=None,max_retry=5,gid=None,
	             send_hup=False,
	             stop_signal=signal.SIGTERM,stop_children=False,env=None,graceful_timeout=30.0,prereload_fn=None,rlimits=None,executable=None,
	             stdout_stream=None,stderr_stream=None,priority=0,loop=None,singleton=False,use_sockets=False,copy_env=False,copy_path=False,
	             max_age=0,max_age_variance=30,hooks=None,respawn=True,autostart=True,on_demand=False,virtualenv=None,stdin_socket=None,
	             close_child_stdin=True,close_child_stdout=False,close_child_stderr=False,virtualenv_py_ver=None,use_papa=False):
		# working_dir=working_dir or default_working_dir
		# virtualenv=virtualenv or virtualenv_root
		# warmup_delay=warmup_delay or watcher_warmup_delay
		# if watcher_respawn is False:
		# 	respawn=watcher_respawn
		if virtualenv: copy_env=True
		self.cmd=cmd
		# region Fields:
		self.name=name
		self.numprocesses=numprocesses
		self.warmup_delay=warmup_delay
		self.working_dir=working_dir
		self.shell=shell
		self.shell_args=shell_args
		self.uid=uid
		self.max_retry=max_retry
		self.gid=gid
		self.send_hup=send_hup
		self.stop_signal=stop_signal
		self.stop_children=stop_children
		self.env=env
		self.graceful_timeout=graceful_timeout
		self.prereload_fn=prereload_fn
		self.rlimits=rlimits
		self.executable=executable
		self.stdout_stream=stdout_stream
		self.stderr_stream=stderr_stream
		self.priority=priority
		self.loop=loop
		self.singleton=singleton
		self.use_sockets=use_sockets
		self.copy_env=copy_env
		self.copy_path=copy_path
		self.max_age=max_age
		self.max_age_variance=max_age_variance
		self.hooks=hooks
		self.respawn=respawn
		self.autostart=autostart
		self.on_demand=on_demand
		self.virtualenv=virtualenv
		self.stdin_socket=stdin_socket
		self.close_child_stdin=close_child_stdin
		self.close_child_stdout=close_child_stdout
		self.close_child_stderr=close_child_stderr
		self.virtualenv_py_ver=virtualenv_py_ver
		self.use_papa=use_papa
		# endregion
		
		TheWatcher.watchers.append(self.to_dict())
	
	def to_dict(self):
		return {k:v for k,v in self.__dict__.items() if v is not None}

class CeleryMan(object):
	
	def __init__(self,celery_path,app_name):
		self.celery_path=celery_path
		self.app_name=app_name
	
	def create_celery_worker(self,worker_name,Ofair=True,queues=None,queue_as_worker_name=True,concurrency=1,autoscale=None,log_level='info',
	                         **watcher_kwargs):
		"""
		This method creates celery worker.
		
		:param worker_name:
					Name of the worker. It will be provided as "-n <worker_name>" argument to celery worker.
		:param Ofair:
					see celery docs.
		:param queues:
					You can specify: 1) single queue (str), 2) list of strings as queue names.
		:param queue_as_worker_name:
					If "queues" is not provided, "worker_name" is used as queue name (by_default).
					If you don't want to specify any queue at all, then pass False.
		:param concurrency:
					Number of concurrent processses. see celery docs.
		:param autoscale:
					Tuple in the form (max,min) processes as specified in celery docs.
		:param log_level:
					Celery log level. By default = "info".
		:param watcher_kwargs:
					Other parameters are passed to TheWatcher.
		:return: Nothing.
		"""
		watcher_name=worker_name+'_watcher'
		parts=list()
		parts.append(f"{self.celery_path} worker -A {self.app_name} -l {log_level}")
		parts.append(f"-n {worker_name}")
		if Ofair: parts.append('-Ofair')
		if queues:
			if type(queues) is str:
				parts.append(f'-Q {queues}')
			else:
				parts.append(f'-Q {",".join(queues)}')
		elif queue_as_worker_name:
			parts.append(f'-Q {worker_name}')
		
		if autoscale:
			parts.append(f"--autoscale={','.join(map(str,autoscale))}")
		else:
			parts.append(f'-c {concurrency}')
		TheWatcher(watcher_name," ".join(parts),**watcher_kwargs)
		pass

def run_watchers():
	arbiter=circus.get_arbiter(TheWatcher.watchers)
	try:
		arbiter.start()
	finally:
		arbiter.stop()
	return

def main():
	"""
	TheWatcher is the main thing that you need for running your commands continuously.
	
		 TheWatcher(name='some_watcher_name',
		            cmd='Command that needs to be run continuously',
		            working_dir='specify_your_working_dir',
		            numprocesses=1,
		            respawn=True)
		 
		 TheWatcher(name='another_watcher_name',
		            cmd='Another command that needs to be run continuously',
		            working_dir='some_other_working_dir',
		            numprocesses=1,
		            respawn=False)
		 
		 run_watchers()
		 
		 That's it. When you call "run_watchers", all declared watchers will be launched in parallel.
		 
		 
	 
	If you need to run celery workers, you can use CeleryMan!:
	
		For example:
			
			cman=CeleryMan(celery_path=r'/usr/local/bin/celery',app_name='celery_worker')
			
			cman.create_celery_worker('get_image_date',autoscale=(18,3))
			cman.create_celery_worker('process_main_request',autoscale=(36,3))

			cman.create_celery_worker('download_products',concurrency=1)
			cman.create_celery_worker('atmospheric_correction_of_single_1c',concurrency=2)
	"""
	TheWatcher('testik','ls -lah',respawn=True) # plohoi primer. Eta commanda ne ranitsya continuously))).
	run_watchers()
	pass

if __name__=='__main__':
	main()
