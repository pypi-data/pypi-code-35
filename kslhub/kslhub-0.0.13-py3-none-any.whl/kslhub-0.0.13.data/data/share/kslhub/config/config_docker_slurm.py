import socket
import os
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
current_host=s.getsockname()[0]
    
print('current_host = %s' % current_host)


c.JupyterHub.admin_users = {"kortass"}

c.JupyterHub.allow_named_servers = False

c.Spawner.debug  = True

c.Authenticator.otp_required = False
c.Authenticator.host = 'ctld'

c.Authenticator.hub_greeting_message = "Welcome to KSL Hub!"
c.Authenticator.hub_name = "Shaheen"
c.Authenticator.job_template_dir = "./job_templates"


c.JupyterHub.authenticator_class = 'kslhub.otp_authenticator.SshUserAuthenticator'
c.JupyterHub.template_paths = [ "%s/share/kslhub/templates" % sys.base_prefix ]



c.JupyterHub.bind_url = 'http://%s:9000' % current_host
c.JupyterHub.hub_bind_url = 'http://%s:9081' % current_host
c.Spawner.cmd = ['jupyter-labhub']


c = get_config()

c.SlurmSpawner.batch_script = '''#!/bin/bash


export JUPYTERHUB_BASE_URL=/
export JUPYTERHUB_CLIENT_ID=jupyterhub-user-__USER__
export JUPYTERHUB_API_TOKEN=__TOKEN__
export JUPYTERHUB_API_URL=http://%s:9081/hub/api
export JUPYTERHUB_USER=__USER__
export JUPYTERHUB_OAUTH_CALLBACK_URL=/user/__USER__/oauth_callback
export JUPYTERHUB_HOST=
export JUPYTERHUB_SERVICE_PREFIX=/user/__USER__/
export CONFIGPROXY_AUTH_TOKEN=__SECRET__

which jupyterhub-singleuser
{cmd}
''' %  (current_host)

c.JupyterHub.spawner_class = 'kslhub.wrapspawner.ProfilesSpawner'
c.Spawner.http_timeout = 120
c.BatchSpawnerBase.req_host = 'localhost'
c.BatchSpawnerBase.req_runtime = '12:00:00'
c.TorqueSpawner.state_exechost_exp = r'in-\1.mesabi.xyz.edu'
c.ProfilesSpawner.profiles = [
   ('Slurm - 1 Node - debug queue - 1 minutes', 'debug01', 'kslhub.batchspawner.SlurmSpawner',
      dict(req_nprocs='1', req_partition='debug', req_runtime='0:01:00')),
   ('Slurm - 1 Node - debug queue - 2 minutes', 'debug02', 'kslhub.batchspawner.SlurmSpawner',
      dict(req_nprocs='1', req_partition='debug', req_runtime='0:02:00')),
   ('Slurm - 1 Node - debug queue - 5 minutes', 'debug05', 'kslhub.batchspawner.SlurmSpawner',
      dict(req_nprocs='1', req_partition='debug', req_runtime='0:05:00')),
   ('Slurm - 1 Node - debug queue - 30 minutes', 'debug30', 'kslhub.batchspawner.SlurmSpawner',
      dict(req_nprocs='1', req_partition='debug', req_runtime='0:30:00')),
   ( "Local server", 'local', 'jupyterhub.spawner.LocalProcessSpawner', {'ip':'0.0.0.0'} ),
   ]

c.InteractiveShellApp.extensions = ['slurm_magic']
c.Spawner.http_timeout = 300
c.Spawner.notebook_dir = '~/NOTEBOOKS' 
c.Spawner.start_timeout = 300
c.Authenticator.admin_users = {"kortass"}
c.PAMAuthenticator.service = 'login'
