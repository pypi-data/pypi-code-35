import os
import sys

c.Authenticator.hub_greeting_message = "Welcome to KSL Hub!"
c.Authenticator.hub_name = "Shaheen"
c.Authenticator.job_template_dir = "./job_templates"
current_host = 'sk.kortas.fr'
#c.JupyterHub.hub_bind_url = 'http://%s:9001' % current_host

c.JupyterHub.authenticator_class = 'kslhub.otp_authenticator.SshUserAuthenticator'
c.Authenticator.otp_required = False 
c.Authenticator.host = 'localhost'

c.JupyterHub.template_paths = [ "%s/share/kslhub/templates" % sys.base_prefix ]

c.Spawner.cmd = ['jupyter-labhub']

runtime_dir = os.path.join('/tmp')


c.JupyterHub.spawner_class = 'kslhub.wrapspawner.ProfilesSpawner'
c.Spawner.http_timeout = 120
c.BatchSpawnerBase.req_host = 'localhost'

# c.ProfilesSpawner.profiles = [
#    ('Slurm - 1 Node - debug queue - 1 minutes', 'debug01', 'batchspawner.SlurmSpawner',
#       dict(req_nprocs='1', req_partition='debug', req_runtime='0:01:00')),
#    ('Slurm - 1 Node - debug queue - 2 minutes', 'debug02', 'batchspawner.SlurmSpawner',
#       dict(req_nprocs='1', req_partition='debug', req_runtime='0:02:00')),
#    ('Slurm - 1 Node - debug queue - 5 minutes', 'debug05', 'batchspawner.SlurmSpawner',
#       dict(req_nprocs='1', req_partition='debug', req_runtime='0:05:00')),
#    ('Slurm - 1 Node - debug queue - 30 minutes', 'debug30', 'batchspawner.SlurmSpawner',
#       dict(req_nprocs='1', req_partition='debug', req_runtime='0:30:00')),
#    ( "Local server", 'local', 'jupyterhub.spawner.LocalProcessSpawner', {'ip':'0.0.0.0'} ),
#    ]

