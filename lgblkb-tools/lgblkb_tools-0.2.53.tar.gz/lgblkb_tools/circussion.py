import circus
import signal

# watcher_conf_override=dict(numprocesses=None,
#                            warmup_delay=None,
#                            working_dir=None,
#                            shell=None,
#                            shell_args=None,
#                            uid=None,
#                            max_retry=None,
#                            gid=None,
#                            send_hup=None,
#                            stop_signal=None,
#                            stop_children=None,
#                            env=None,
#                            graceful_timeout=None,
#                            prereload_fn=None,
#                            rlimits=None,
#                            executable=None,
#                            stdout_stream=None,
#                            stderr_stream=None,
#                            priority=None,
#                            loop=None,
#                            singleton=None,
#                            use_sockets=None,
#                            copy_env=None,
#                            copy_path=None,
#                            max_age=None,
#                            max_age_variance=None,
#                            hooks=None,
#                            respawn=None,
#                            autostart=None,
#                            on_demand=None,
#                            virtualenv=None,
#                            stdin_socket=None,
#                            close_child_stdin=None,
#                            close_child_stdout=None,
#                            close_child_stderr=None,
#                            virtualenv_py_ver=None,
#                            use_papa=None,
#                            )

watcher_conf_override={'numprocesses':None,'warmup_delay':None,'working_dir':None,'shell':None,'shell_args':None,'uid':None,'max_retry':None,'gid':None,'send_hup':None,
                       'stop_signal':None,'stop_children':None,'env':None,'graceful_timeout':None,'prereload_fn':None,'rlimits':None,'executable':None,'stdout_stream':None,
                       'stderr_stream':None,'priority':None,'loop':None,'singleton':None,'use_sockets':None,'copy_env':None,'copy_path':None,'max_age':None,'max_age_variance':None,
                       'hooks':None,'respawn':None,'autostart':None,'on_demand':None,'virtualenv':None,'stdin_socket':None,'close_child_stdin':None,'close_child_stdout':None,
                       'close_child_stderr':None,'virtualenv_py_ver':None,'use_papa':None}

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
		self.name=name
		# region Fields:
		self.numprocesses=watcher_conf_override['numprocesses'] or numprocesses
		self.warmup_delay=watcher_conf_override['warmup_delay'] or warmup_delay
		self.working_dir=watcher_conf_override['working_dir'] or working_dir
		self.shell=watcher_conf_override['shell'] or shell
		self.shell_args=watcher_conf_override['shell_args'] or shell_args
		self.uid=watcher_conf_override['uid'] or uid
		self.max_retry=watcher_conf_override['max_retry'] or max_retry
		self.gid=watcher_conf_override['gid'] or gid
		self.send_hup=watcher_conf_override['send_hup'] or send_hup
		self.stop_signal=watcher_conf_override['stop_signal'] or stop_signal
		self.stop_children=watcher_conf_override['stop_children'] or stop_children
		self.env=watcher_conf_override['env'] or env
		self.graceful_timeout=watcher_conf_override['graceful_timeout'] or graceful_timeout
		self.prereload_fn=watcher_conf_override['prereload_fn'] or prereload_fn
		self.rlimits=watcher_conf_override['rlimits'] or rlimits
		self.executable=watcher_conf_override['executable'] or executable
		self.stdout_stream=watcher_conf_override['stdout_stream'] or stdout_stream
		self.stderr_stream=watcher_conf_override['stderr_stream'] or stderr_stream
		self.priority=watcher_conf_override['priority'] or priority
		self.loop=watcher_conf_override['loop'] or loop
		self.singleton=watcher_conf_override['singleton'] or singleton
		self.use_sockets=watcher_conf_override['use_sockets'] or use_sockets
		self.copy_env=watcher_conf_override['copy_env'] or copy_env
		self.copy_path=watcher_conf_override['copy_path'] or copy_path
		self.max_age=watcher_conf_override['max_age'] or max_age
		self.max_age_variance=watcher_conf_override['max_age_variance'] or max_age_variance
		self.hooks=watcher_conf_override['hooks'] or hooks
		self.respawn=watcher_conf_override['respawn'] or respawn
		self.autostart=watcher_conf_override['autostart'] or autostart
		self.on_demand=watcher_conf_override['on_demand'] or on_demand
		self.virtualenv=watcher_conf_override['virtualenv'] or virtualenv
		self.stdin_socket=watcher_conf_override['stdin_socket'] or stdin_socket
		self.close_child_stdin=watcher_conf_override['close_child_stdin'] or close_child_stdin
		self.close_child_stdout=watcher_conf_override['close_child_stdout'] or close_child_stdout
		self.close_child_stderr=watcher_conf_override['close_child_stderr'] or close_child_stderr
		self.virtualenv_py_ver=watcher_conf_override['virtualenv_py_ver'] or virtualenv_py_ver
		self.use_papa=watcher_conf_override['use_papa'] or use_papa
		# endregion
		
		TheWatcher.watchers.append(self.to_dict())
	
	def to_dict(self):
		return {k:v for k,v in self.__dict__.items() if v is not None}

class CeleryMan(object):
	
	def __init__(self,celery_path,app_name):
		self.celery_path=celery_path
		self.app_name=app_name
	
	def create_celery_worker(self,worker_name,Ofair=True,queues=None,queue_as_worker_name=True,
	                         concurrency=1,autoscale=None,log_level='info',add_cmd='',**watcher_kwargs):
		"""
		This method creates celery worker.
		
		:param add_cmd: Additional cmd to add manually to the end of constructed cmd.
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
		TheWatcher(watcher_name," ".join([*parts,add_cmd]),**watcher_kwargs)
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
	TheWatcher('testik','ls -lah',respawn=True)  # plohoi primer. Eta commanda ne ranitsya continuously))).
	run_watchers()
	pass

if __name__=='__main__':
	main()
