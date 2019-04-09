#	Copyright (C) 2019, Mentice AB
#	See accompanying LICENSE file

import asyncio
import codecs
import os
import pickle
import shlex
import signal
from asyncio.subprocess import PIPE, STDOUT
from datetime import datetime

import async_timeout
import docker

import jobber


def split_pipeline(pipeline):
	pipeline = shlex.split(pipeline)
	pipes = [i for i in range(len(pipeline)) if pipeline[i] == '|']
	j = 0
	cmds = []
	for i in pipes:
		cmds.append(pipeline[j:i])
		j = i+1
	cmds.append(pipeline[j:])
	return cmds

def timestamp():
	"""Return a string with format YYYYMMDD-HHMMSS
	"""
	return datetime.utcnow().strftime('%Y%m%d_%H%M%S')

def is_sha256(str):
	"""Return True if str is a 64-byte hex string
	"""
	try:
		int(str, 16)
		return True
	except:
		return False

def strip_sha256(id):
	"""Strip off 'sha256' from 'sha256:xxxx...'
	"""
	if id.startswith('sha256:'):
		return id[7:]
	else:
		return id

def parse_tag(tag):
	"""Parse a docker tag into a path, name, and tag

	Docker tags may specify a registry host, port and path, a repository name, and a tag
	Returns: (path, name, tag)
		path will end with '/', or equal '' if there is no path
		tag may be ''
	Examples:
		example.com:5000/data/mnist-data:latest
			path: 'example.com:5000/data/'
			name: 'mnist-data'
			tag:  'latest'
		hello
			path: ''
			name: 'hello'
			tag:  ''
	"""
	paths = tag.split('/')
	path, name = '/'.join(paths[:-1]), paths[-1]
	if path:
		path = path + '/'
	names = name.split(':')
	if len(names) == 1:
		name, tag = names[0], ''
	elif len(names) == 2:
		name, tag = names
	else:
		raise ValueError("{0}: bad tag".format(tag))
	return path, name, tag

def make_tag(path, name, tag):
	"""Construct a string from (path, name, tag)
	
	Essentially the opposite of parse_tag()"""
	if path and path.endswith('/'):
		path = path[:-1]

	if path:
		if name:
			if tag:
				return '{path}/{name}:{tag}'.format(path=path, name=name, tag=tag)
			else:
				return '{path}/{name}'.format(path=path, name=name)
		else:
			raise ValueError('Invalid tag: missing name')
	else:
		if name:
			if tag:
				return '{name}:{tag}'.format(name=name, tag=tag)
			else:
				return name
		else:
			raise ValueError('Invalid tag: missing name')


def add_standard_tags(tags):
	"""Add standard tag names to tags list for each registry path (if any)
		name:YYYYMMDD-HHMMSS
		name:latest
	
	Don't add standard tags if user specified a fully qualified name:tag
	"""
	tags = list(tags)
	paths = {}      # Set of tags for each unique "path/name" 
	for tag in tags:
		path, name, tag = parse_tag(tag)
		path = path + name
		if not path in paths:
			paths[path] = set()
		if tag:
			paths[path].add(tag)
		else:
			paths[path].add('latest')

	if len(tags) == 0:
		name = os.path.basename(os.getcwd())    # Default name is directory name
		paths[name] = set()
	for path, tag_set in paths.items():
		if len(tag_set - {'latest'}) == 0:
			tag_set.add('{0}'.format(timestamp()))
			tag_set.add('latest')

	tags = []
	for path, tag_set in paths.items():
		for tag in tag_set:
			if tag:
				tags.append('{0}:{1}'.format(path, tag))
			else:
				tags.append(path)
	return tags

def add_default_registry(default_registry, arg):
	"""Prepend arg (or each element of arg if its a list) with the default_registry

	Returns a list if arg is a list, or a string if arg is a string
	"""
	if not default_registry:
		return arg
	def prepend_registry(tag):
		path, name, tag = parse_tag(tag)
		if path:        # Nothing to add if it already has a path
			return make_tag(path, name, tag)
		else:
			return make_tag(default_registry, name, tag)
	if type(arg) is list:
		return list(map(prepend_registry, arg))
	else:
		return prepend_registry(arg)

def validate_dir_name(dir_name):
	if not dir_name.startswith('/'):
		raise ValueError('"{0}": directory name must begin with "/"'.format(dir_name))

def first_line(s):
	"""Return first full line from string s (not including the '\n')
	"""
	i = s.find('\n')
	if i > 0:
		return s[:i]
	else:
		raise RuntimeError("can't find '\\n' in first_line")


class RunError(Exception):
	"""An error occurred while running a subprocess
	"""
	def __init__(self, mesg, return_code, log=None):
		self.mesg = mesg
		self.return_code = return_code
		self.log = log

	def __str__(self):
		return self.mesg


class Jobber(object):
	"""Docker Jobber
	"""
	def __init__(self, config):
		"""config: a dict containing config options
		"""
		self.config = config
		self.docker_client = docker.DockerClient(base_url=self._get_host())
		self._set_run_state(None)
		if os.name == 'nt':     # Windows
			loop = asyncio.ProactorEventLoop()
			asyncio.set_event_loop(loop)

	@property
	def verbose(self):
		return self.config['verbose']
	
	def build_image(self, path, tags=(), dockerfile='Dockerfile'):
		async def code():
			nonlocal tags, dockerfile
			host = self._get_host(option=True)
			
			tags = add_standard_tags(tags)
			tags = add_default_registry(self.config['registry'], tags)

			if dockerfile == None:
				dockerfile = 'Dockerfile'

			tag_str = ' '.join(map(lambda x: "-t {0}".format(x), tags))
			cmd = 'docker {host} build --label="jobber.build-tags={tags}" --label="jobber.version={version}" --rm --force-rm -f {0} {1} {2}'.format(dockerfile, tag_str, path, host=host, tags=tags, version=jobber.__version__)
			await self._exec(cmd, echo=self.verbose)

			# Push to registries
			return await self._push_tags(tags, host=host)
		return self._run_loop(self._try, code, 'The build failed', print_log=not self.verbose)

	def run_image(self, image_name):
		async def code():
			config = self.config.copy()
			host = self._get_host(option=True)
			if host:
				config['host'] = ''
			if config['out']:
				validate_dir_name(config['out'])
			jobber_runner = "mentice/jobber-runner:{version}".format(version=jobber.__version__)
			config_b64 = codecs.encode(pickle.dumps(config), "base64").decode()
			cmd = 'docker {host} run -it --rm --env JOBBER_CONFIG="{config}" -v /var/run/docker.sock:/var/run/docker.sock {jobber_runner} {image_name}'.format(host=host, config=config_b64, image_name=image_name, jobber_runner=jobber_runner)
			await self._exec(cmd, echo=True)
			return 0    # Return code. _run() raises RunError if return code not 0.
		return self._run_loop(self._try, code, 'Execution failed', print_log=False)

	def _get_host(self, option=False):
		"""Return '-H <host>' command line option
		"""
		host = self.config['host']
		if host:
			port = 2375     # Default docker port
			sp = host.rsplit(':', 1)
			if len(sp) == 2:
				try:
					port = int(sp[1])
				except:
					pass
			host = '{host}:{port}'.format(host=sp[0], port=port)
			if option:
				host = '-H '+host
		return host

	def launch(self, image_name, **kwargs):
		"""Manage launching of a user image.
		Called from runner.py
		"""
		return self._run_loop(self._launch, image_name, **kwargs)
	
	async def _get_image(self, image_name, pull=False):
		"""Get Image object from an image name
		"""
		path, name, tag = parse_tag(image_name)
		if pull and path:
			return await self._pull(image_name)
		else:
			return self.docker_client.images.get(image_name)

	async def _pull(self, image_name):
		"""Attempt to pull an image
		"""
		async def code():
			await self._exec('docker pull {0}'.format(image_name))
			return await self._get_image(image_name)
		return await self._try(code, 'Unable to pull image', error_code=None)
		
	async def _push(self, image_name, host=''):
		"""Attempt to push an image
		"""
		async def code():
			await self._exec('docker {host} push {0}'.format(image_name, host=host))
			if not self.verbose:
				print('Pushed {0}'.format(image_name))
			return 0
		return await self._try(code, 'Unable to push {0}'.format(image_name))

	async def _push_tags(self, tags, host=''):
		"""Push tags with registry specs
		"""
		for tag in tags:
			path, name, tag = parse_tag(tag)
			if path and tag:
				if await self._push(make_tag(path, name, tag), host):
					return 1
		return 0

	async def _launch(self, image_name):
		image_name = add_default_registry(self.config['registry'], image_name)

		config = self.config
		inputs = config['inputs']
		out = config['out']

		# Login to google cloud if any image or volume references grc.io
		gcr_io = image_name.startswith("gcr.io/")
		for vol in inputs:
			if vol.startswith("gcr.io/"):
				gcr_io = True
		if out and out.startswith("gcr.io/"):
			gcr_io = True
		if gcr_io:
			await self._exec('cat gcr_key.json | docker login -u _json_key --password-stdin https://gcr.io')

		image = await self._get_image(image_name, pull=True)
		if not image:
			if not self.verbose:
				print('Image not found')
			return 1

		image_id = strip_sha256(image.id)

		# Use image_name as base name for generating tags for the result image after a successful run
		path, name, _ = parse_tag(image_name)
		base_name = path + name
		if is_sha256(base_name):
			base_name = None

		container_id = None
		return_code = 0
		vols = None

		def sigint():
			if self.run_state and self.interrupts == 0:
				self.interrupts += 1
				print('Job {0}. Type ^C again to abort immediately.'.format(self.run_state))
			else:
				print('KeyboardInterrupt')
				exit(-int(signal.SIGINT))
		asyncio.get_event_loop().add_signal_handler(signal.SIGINT, sigint)

		async def launch():
			nonlocal vols, container_id
			cmd = 'docker create -it --runtime={runtime}'.format(runtime=config['runtime'])
			if len(inputs) > 0:
				vols = await self._load_input_volumes(inputs)
				for vol in vols:
					cmd += ' -v {0}'.format(vol)

			# Convert cmd from a string to a list of list of strings
			cmds = split_pipeline(cmd)

			# Pass along docker options
			if 'Xdocker' in config:
				for xdocker in config['Xdocker']:
					if type(xdocker) is str:
						xdocker = shlex.split(xdocker)
					cmds[-1] += xdocker

			# Image to run
			cmds[-1].append(image_id)

			# CMD override
			if 'cmd' in config:
				cmds[-1] += config['cmd']

			self._set_run_state('starting')
			try:
				log = await self._exec(cmds)
			except RunError as e:
				print(e.log, end='')
				raise e

			container_id = first_line(log)

			def postexec_fn():
				self._set_run_state('terminating')
			await self._exec('docker start -a -i=true {0}'.format(container_id), timeout=config['timeout'], echo=True, postexec_fn=postexec_fn)

		def report_error(e):
			nonlocal return_code
			if e:
				if isinstance(e, RunError):
					return_code = e.return_code
				else:
					return_code = 1
					print('{0} {1}'.format(type(e), e))

		async def cleanup(e=None):
			report_error(e)
			# Attempt to clean up container
			async def code():
				if container_id:
					try:
						await self._exec('docker kill {0}'.format(container_id))
					except RunError:
						pass
					finally:
						await self._exec('docker rm {0}'.format(container_id))
			await self._try(code)

		async def finalize(e=None):
			report_error(e)
			async def code():
				try:
					await self._exec('docker kill {0}'.format(container_id))
				except RunError:
					pass

				log = await self._exec("docker inspect {0} --format='{{{{.State.ExitCode}}}}'". format(container_id))
				return_code = int(first_line(log))

				await self._save_log(container_id, container_id, "run.log")

				# Server log
				log = await self._exec('cat /proc/self/cgroup | grep -e docker | head -1 | cut -d/ -f3')
				server_id = first_line(log)
				await self._save_log(server_id, container_id, "server.log")

				labels = {'jobber.version':jobber.__version__, 'jobber.parent':image_id}
				if out:
					labels['jobber.out'] = out
				if len(inputs) > 0:
					labels['jobber.inputs'] = ','.join(vols)
				label_str = ' '.join(map(lambda item: '''-c "LABEL {key}='{val}'"'''.format(key=item[0], val=item[1]), labels.items()))

				if base_name:
					now = timestamp()
					tags = (
						'{base_name}:latest-run'.format(base_name=base_name), 
						'{base_name}:{timestamp}'.format(base_name=base_name, timestamp=now)
					)
					log = await self._exec('docker commit {0} {1} {tag}'.format(label_str, container_id, tag=tags[0]))
					for tag in tags[1:]:
						await self._exec('docker tag {0} {tag}'.format(strip_sha256(first_line(log)), tag=tag))

					if path:        # Push to registries
						for tag in tags:
							if await self._push('{tag}'.format(tag=tag)):
								return_code = 1
								break
				else:
					log = await self._exec('docker commit {0} {1}'.format(label_str, container_id))

				await self._exec('docker rm {0}'.format(container_id))
				self._set_run_state(None)
				return return_code
			nonlocal return_code
			return_code = await self._try(code, 'Unable to finalize container', error_code=1, print_log=True)

		try:
			await launch()
		except Exception as e:
			if container_id and self.config['result-image'] == 'always':
				await finalize(e)
			else:
				await cleanup(e)
		else:   # run completed: get exit code
			if self.config['result-image'] == 'success' or self.config['result-image'] == 'always':
				await finalize()
			else:
				await cleanup()

		return return_code

	def _set_run_state(self, state):
		# print('_set_run_state({0})'.format(state))
		self.run_state = state
		self.interrupts = 0

	async def _save_log(self, container_id, user_id, filename):
		await self._exec('docker logs {0} > /tmp/jobber_logs/{1}'.format(container_id, filename))
		await self._exec('docker cp /tmp/jobber_logs/{0} {1}:/{0}'.format(filename, user_id))

	async def _load_input_volumes(self, vols):
		"""Verify or build volumes in 'vols' list.

		Input volumes are mounted read-only
		vol format:
			<image>[,src=/src-dir][,dest=/dest-dir]   # src-dir defaults to image's out label; dest-dir defaults to '/data'

		Returns a list of valid volume names suitable for the docker '-v' command line option.
		"""
		ret = []
		for vol in vols:
			split = vol.split(',')
			src_dir, dest_dir = None, '/data'
			if len(split) > 0:
				image_name = split[0]
				if len(split) > 1:
					for item in split[1:]:
						pair = item.split('=')
						if len(pair) != 2:
							raise ValueError('Invalid input volume format: "{0}"'.format(vol))
						key, val = pair
						if key == 'src' or key == 'source':
							src_dir = val
						elif key == 'dest' or key == 'local':
							dest_dir = val
						else:
							raise ValueError('Invalid input volume format: "{0}"'.format(vol))
				if src_dir:
					validate_dir_name(src_dir)
				validate_dir_name(dest_dir)
			else:
				raise ValueError('Invalid input volume format: "{0}"'.format(vol))

			image_name = add_default_registry(self.config['registry'], image_name)
			image = await self._get_image(image_name, pull=True)
			if not image:
				raise ValueError("{0}: Can't find input image".format(image_name))
			try:
				if src_dir:
					vol_name = image.id + src_dir.replace('/', '.')
				else:
					vol_name = image.id
				vol_name = strip_sha256(vol_name)

				docker_vol = self.docker_client.volumes.get(vol_name)
				spec = '{0}:{1}:ro'.format(docker_vol.id, dest_dir)
			except Exception:  # Volume not found - attempt to create it
				print('Creating volume {0}'.format(vol_name))

				if not src_dir:
					labels = image.labels
					if 'jobber.out' not in labels:
						src_dir = '/data'
					else:
						src_dir = labels['jobber.out']

				# Create and destroy a temporary container to create the volume. Don't start the container.
				log = await self._exec('docker create -v {vol_name}:{src_dir} {id}'.format(vol_name=vol_name, src_dir=src_dir, id=image.id))
				container_id = first_line(log)
				await self._exec('docker rm {0}'.format(container_id))

				docker_vol = self.docker_client.volumes.get(vol_name)
				spec = '{0}:{1}:ro'.format(docker_vol.id, dest_dir)
			ret.append(spec)
		return ret

	def _run(self, cmd, **kwargs):
		"""Run a pipeline of commands asynchronously. Wait until all commands complete.
		"""
		return self._run_loop(self._exec, cmd, **kwargs)

	def _run_loop(self, func, *args, **kwargs):
		loop = asyncio.get_event_loop()
		ret = loop.run_until_complete(func(*args, **kwargs))
		return ret

	async def _exec(self, pipeline, stdin=None, verbose=None, echo=False, timeout=None, postexec_fn=None):
		"""Execute a pipeline of commands returning the output from the last command.

		pipeline -- either a string or list of lists of commands

		Examples:
			_exec('head -c 1000 /dev/urandom | od -h | wc')
			_exec([['head', '-c', '1000', '/dev/urandom'], ['od', '-h'], ['wc']])
		"""
		if verbose is None:
			verbose = self.verbose

		if type(pipeline) is list:
			cmds = pipeline
		else:
			cmds = split_pipeline(pipeline)
		if verbose:
			print('|'.join([' '.join(cmd) for cmd in cmds]))

		# Check for redirected output of last command
		outf = None
		last = cmds[-1]
		if len(last) > 2 and last[-2] == '>':
			path = last[-1]
			os.makedirs(os.path.dirname(path), exist_ok=True)
			outf = open(path, 'w')
			cmds[-1] = last[:-2]

		# Start the pipeline
		last = cmds[-1]
		for cmd in cmds:
			# Have to use explicit pipes (see https://stackoverflow.com/questions/36657753/connect-two-processes-started-with-asyncio-subprocess-create-subprocess-exec/36666420)
			if cmd is last:
				stdout, stderr = PIPE, STDOUT
			else:
				pread, pwrite = os.pipe()
				stdout = stderr = pwrite
			def preexec():
				"""Ignore SIGINT in the subprocess"""
				signal.signal(signal.SIGINT, signal.SIG_IGN)
			if os.name == 'nt':     # Windows
				proc = await asyncio.create_subprocess_exec(*cmd, stdin=stdin, stdout=stdout, stderr=stderr)
			else:
				proc = await asyncio.create_subprocess_exec(*cmd, stdin=stdin, stdout=stdout, stderr=stderr, preexec_fn=preexec)
			if stdin is not None:
				os.close(stdin)
			if cmd is not last:
				os.close(pwrite)
				stdin = pread

		if postexec_fn:
			postexec_fn()

		# Read output of last command
		log = ''
		async with async_timeout.timeout(timeout):
			while True:
				data = await proc.stdout.read(2**16)
				if len(data) == 0: 
					break
				data = data.decode()
				if outf is not None:
					outf.write(data)
				else:
					log += data		# Apparently this isn't O(n^2). nice.
				if echo:
					print(data, end='', flush=True)
			await proc.wait()
			if proc.returncode != 0:
				raise RunError('Process exited with {0}'.format(proc.returncode), proc.returncode, log=log)
		return log

	async def _try(self, code, mesg=None, error_code=1, print_log=None):
		if print_log is None:
			print_log = self.verbose
		try:
			return await code()
		except RunError as e:
			if print_log:
				print(e.log, end='')
			if mesg:
				print('{mesg}: {e}'.format(mesg=mesg, e=e))
			return error_code
		except Exception as e:
			if mesg:
				print('{mesg}: {type} {e}'.format(mesg=mesg, type=type(e), e=e))
			return error_code
