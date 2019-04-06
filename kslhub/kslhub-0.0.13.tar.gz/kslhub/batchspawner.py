# Copyright (c) Regents of the University of Minnesota
# Copyright (c) Michael Gilbert
# Distributed under the terms of the Modified BSD License.

"""Batch spawners

This file contains an abstraction layer for batch job queueing systems, and implements
Jupyterhub spawners for Torque, SLURM, and eventually others.

Common attributes of batch submission / resource manager environments will include notions of:
  * queue names, resource manager addresses
  * resource limits including runtime, number of processes, memory
  * singleuser child process running on (usually remote) host not known until runtime
  * job submission and monitoring via resource manager utilities
  * remote execution via submission of templated scripts
  * job names instead of PIDs
"""
import asyncio
from concurrent.futures import ThreadPoolExecutor
import os
import pprint
import pwd
import re
import signal
from subprocess import Popen, call
import subprocess
import sys, traceback
from urllib.parse import quote, urlparse

from tornado import gen
from tornado.iostream import StreamClosedError
from tornado.process import Subprocess
from traitlets import (
    Instance, Integer, Unicode, Float, Dict
)

from kslhub.ssh_authenticator import session_manager
from jupyterhub import dbutil, orm
from jupyterhub.app import JupyterHub
from jupyterhub.spawner import Spawner
from jupyterhub.spawner import set_user_setuid
from jupyterhub.utils import random_port
import xml.etree.ElementTree as ET

from kslhub import scan_template
import glob
import re

# add on to compute secret and token to be passed to the spawning job
# import os
# from jupyterhub.services.auth import HubAuth
# auth = HubAuth(
#     api_token=os.environ['JUPYTERHUB_API_TOKEN'],
#     cookie_cache_max_age=60,
# )
kslhub_root = "."  # os.getenv('KSLHUB_ROOT')

slurm_machine = session_manager()

@gen.coroutine
def run_command(cmd, input=None, env=None, user=None):
    print("SKKKKKKKKKk cmd run : |||%s||| " % cmd)
    #print("SKKKKKKKKKk env : |||%s||| " % pprint.pformat(env))
    #print("SKKKKKKKKKk cmd : |||%s||| " % pprint.pformat(cmd))
    #input_str = "|||%s||| " % pprint.pformat(input)
    #print("SKKKKKKKKKk input : %s, find_result: %s" % (input_str, input_str.find("|||None|||")))
    print("[AUTHENT]================ here user=%s!!!" % user)
    print("[AUTHENT] slurm_machine=%s   or %s" % (slurm_machine,pprint.pformat(slurm_machine)))
    if user==None:
        print("[AUTHENT]===============  here user=None!!!")
        traceback.print_stack()
        print("[AUTHENT]===============  here user=None!!!")
    try:
        connection = slurm_machine.get_session(user)
        if not(connection):
            print("[AUTHENT]==================== session expired for %s/%s " %\
                  (slurm_machine.machine,user))
            traceback.print_stack()
            print("[AUTHENT]==================== session expired for %s/%s " %\
                  (slurm_machine.machine,user))
            return False
            # test de la connection
            return redirect(auth.login_url + '?next=%s' % quote(request.path))
  
    except Exception as e:
        print("[AUTHENT] no connection: problem in getting the session")
        print(e)
        traceback.print_exc(file=sys.stdout)
        return "problem starting ssh session"
        
    stdin, stdout, stderr = connection.exec_command(cmd)
    if not(input==None):
        print("sending input:/%s/" % input)
        stdin.write("".join(input))
        stdin.channel.shutdown_write()
    else:
        print("[AUTHENT] no input")
 
        
    output = stdout.readlines()
    print("[AUTHENT] output for cmd=|||%s||| = %s " %    (cmd,output))
    try:
        res = output[-1][:-1]
    except:
        print("[AUTHENT] problem in parsing output. forcing res at nothing")
        res = ""
    print("[AUTHENT] res for cmd=|||%s||| = %s " %    (cmd,res))
    return res


class BatchSpawnerBase(Spawner):
    """Base class for spawners using resource manager batch job submission mechanisms

    This base class is developed targetting the TorqueSpawner and SlurmSpawner, so by default
    assumes a qsub-like command that reads a script from its stdin for starting jobs,
    a qstat-like command that outputs some data that can be parsed to check if the job is running
    and on what remote node, and a qdel-like command to cancel a job. The goal is to be
    sufficiently general that a broad range of systems can be supported with minimal overrides.

    At minimum, subclasses should provide reasonable defaults for the traits:
        batch_script
        batch_submit_cmd
        batch_query_cmd
        batch_cancel_cmd

    and must provide implementations for the methods:
        state_ispending
        state_isrunning
        state_gethost
    """

    # override default since batch systems typically need longer
    start_timeout = Integer(300, config=True)

    # override default server ip since batch jobs normally running remotely
    ip = Unicode("0.0.0.0", config=True, help="Address for singleuser server to listen at")

    # all these req_foo traits will be available as substvars for templated strings
    req_queue = Unicode('', config=True, \
        help="Queue name to submit job to resource manager"
        )

    req_host = Unicode('', config=True, \
        help="Host name of batch server to submit job to resource manager"
        )

    req_memory = Unicode('', config=True, \
        help="Memory to request from resource manager"
        )

    req_nprocs = Unicode('', config=True, \
        help="Number of processors to request from resource manager"
        )

    req_runtime = Unicode('', config=True, \
        help="Length of time for submitted job to run"
        )

    req_options = Unicode('', config=True, \
        help="Other options to include into job submission script"
        )

    hub_port = Integer(8080, config=True, \
        help="Port where the hub is talking"
        )

    hub_ip = Unicode('localhost', config=True, \
        help="IP of the hub"
        )

    proxy_port = Integer(8081, config=True, \
        help="Port where the proxy is talking"
        )

    proxy_ip = Unicode('localhost', config=True, \
        help="IP of the proxy"
        )

    req_username = Unicode()
    def _req_username_default(self):
        return self.user.name

    # Useful IF getpwnam on submit host returns correct info for exec host
    req_homedir = Unicode()
    def _req_homedir_default(self):
        return pwd.getpwnam(self.user.name).pw_dir

    req_keepvars = Unicode()
    def _req_keepvars_default(self):
        return ','.join(self.get_env().keys())

    batch_script = Unicode('', config=True, \
        help="Template for job submission script. Traits on this class named like req_xyz "
             "will be substituted in the template for {xyz} using string.Formatter. "
             "Must include {cmd} which will be replaced with the jupyterhub-singleuser command line."
        )

    # Raw output of job submission command unless overridden
    job_id = Unicode()

    # Will get the raw output of the job status command unless overridden
    job_status = Unicode()

    # Prepare substitution variables for templates using req_xyz traits
    def get_req_subvars(self):
        names = self.trait_names()
        reqlist = [ t for t in self.trait_names() if t.startswith('req_') ]
        # need to add req_input manually..
        for k,v in self.__dict__.items():
            if k[:4] == "dyn_":
               reqlist = reqlist + [k]
        subvars = {}
        for t in reqlist:
            subvars[t[4:]] = getattr(self, t)
        return subvars

    batch_submit_cmd = Unicode('', config=True, \
        help="Command to run to submit batch scripts. Formatted using req_xyz traits as {xyz}."
        )

    def parse_job_id(self, output):
        "Parse output of submit command to get job id."
        return output

    def cmd_formatted_for_batch(self):
        return ' '.join(self.cmd + self.get_args())

    @gen.coroutine
    def submit_batch_script(self):
        subvars = self.get_req_subvars()
        cmd = self.batch_submit_cmd.format(**subvars)
        self.log.info("\nsubvars:%s\n" % pprint.pformat(subvars))
        
        for v in subvars['keepvars'].split(","):
            if os.getenv(v):
                subvars[v] = os.getenv(v)

        self.log.info("\nsubvars after keepvar :%s\n" % pprint.pformat(subvars))
        
        #SKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKkkk
        template_directory = '%s/' % self.authenticator.job_template_dir
        template_to_find =  "%s/%s -*.template" % (template_directory,subvars['input'])
        self.log.info('template_to_find: /%s/' % template_to_find)

        templates = glob.glob(template_to_find)

        template = templates[0]

        self.log.info("template found %s" % template)

        script = "".join(open(template,"r").readlines())
        
        self.log.info('template content: \n' + '='*80 + '\n' + script + '\n' + '='*80 + '\n')

        # replace all the __tag;...;..;;...__ and __tag__ pattern with the value
        # chosen in the GUI
        
        for k in subvars.keys():
            v = subvars[k]
            script = re.sub(r"__%s;.+__" % k , v, script)
            script = re.sub(r"__%s__" % k , v, script)
            
        self.log.info('content after __tag__ replacememnt: \n' \
                      + '='*80 + '\n' + script + '\n' + '='*80 + '\n')
        
        self.log.info('user_options: %s' % self.user_options)


        # initialize the keepvar environment variable

        # find the right spot in the script (just before the first command

        script_env_set = ""
        env_done = False
        for l in script.split("\n"):
            if len(l)==0:
                script_env_set = script_env_set + l + "\n"
            elif l[0]=="#" or len(l.strip())==0 or env_done:
                script_env_set = script_env_set + l + "\n"
            else:
                vars = "#" * 80 + "\n# Environment variables to be forwarded....\n"
                for v in subvars['keepvars'].split(","):
                    if os.getenv(v):
                        vars = vars + "export %s=%s\n " % (v,os.getenv(v))
                vars = vars + "#" * 80 + "\n"
                script_env_set = script_env_set + vars

                # adding token and secret credential

                script_env_set = script_env_set + """
                export JUPYTERHUB_BASE_URL=/
                export JUPYTERHUB_CLIENT_ID=jupyterhub-user-__USER__
                export JUPYTERHUB_API_TOKEN=__TOKEN__
                export JUPYTERHUB_API_URL=http://__HOST__:__PORT__/hub/api
                export JUPYTERHUB_USER=__USER__
                export JUPYTERHUB_OAUTH_CALLBACK_URL=/user/__USER__/oauth_callback
                export JUPYTERHUB_HOST=
                export JUPYTERHUB_SERVICE_PREFIX=/user/__USER__/
                export CONFIGPROXY_AUTH_TOKEN=__SECRET__
                export PYTHONPATH=__PYTHONPATH__
                """ + "#" * 80 + "\n"
                
                env_done = True
                

        script = script_env_set
        self.log.info('content after env addition: \n' \
                      + '='*80 + '\n' + script + '\n' + '='*80 + '\n')


        
        # computing the token related to user
        
        hub = JupyterHub(parent=self)
        hub.load_config_file(hub.config_file)
        hub.init_db()
        def init_users():
            loop = asyncio.new_event_loop()
            loop.run_until_complete(hub.init_users())
        ThreadPoolExecutor(1).submit(init_users).result()
        user = orm.User.find(hub.db, self.user.name)
        self.log.info("user : %s" % pprint.pformat(self.user))
        if user is None:
            self.log.info("No such user: %s" % self.user.name, file=sys.stderr)
            self.exit(1)
        token = user.new_api_token(note="command-line generated")
        print(token)
        
        self.log.info("token = !!!%s!!! " % token)

        script = script.replace("__TOKEN__",token)


        client_id = 'jupyterhub-user-%s' % quote(self.user.name)
        oauth_client = (
            hub.db
            .query(orm.OAuthClient)
            .filter_by(identifier=client_id)
            .first()
        )
        self.log.info("secret = !!!%s!!! " % oauth_client.secret)

        script = script.replace("__SECRET__", oauth_client.secret)
        script = script.replace("__USER__", self.user.name)
        # SKKKKKKKK to be fixed!!!
        script = script.replace("__HOST__", self.proxy_ip)
        script = script.replace("__PORT__", str(self.proxy_port))
        script = script.replace("__NOTEBOOK_PORT__",str(self.user.server.port))
        if os.getenv("PYTHONPATH"):
            script = script.replace("__PYTHONPATH__", os.getenv("PYTHONPATH"))
        

        self.log.info('content after token replacement: \n' \
                      + '='*80 + '\n' + script + '\n' + '='*80 + '\n')

        
        
        subvars['cmd'] = self.cmd_formatted_for_batch()
        self.log.info("cmd formatted:%s" % subvars['cmd'])
        script = script.replace("__CONNECT__", subvars['cmd'])
        
        if hasattr(self, 'user_options'):
            subvars['user_options'] = self.user_options

        #script = self.batch_script.format(**subvars)
        #self.log.debug('Spawner submitting job using ' + cmd)
        #self.log.debug('Spawner submitted script:\n' + script)


        # set all 
        
            
        f = open("%s/jobs/%s_last_script" %  (kslhub_root,self.user.name),"w")
        f.write(script)
        f.close()



        if script.find("#SBATCH -v")>-1:
            # need to export environment variable by dynamically computing their absolute values
            vars = "#" * 80 + "\n# Environment variable to be forwarded....\n"
            for v in subvars['keepvars'].split(","):
                if os.getenv(v):
                    vars = vars + "export %s=%s\n " % (v,os.getenv(v))
            vars = vars + "#" * 80 + "\n"

            script = script.replace("#SBATCH -v","###########SBATCH -v")
            #script = script.replace("\njupyterhub-singleuser","\n"+vars+"\njupyterhub-singleuser  --config=/home/kortass/JUPYTER/jupyterhub_config.py")
            script = script.replace("\njupyterhub-singleuser","\n"+vars+\
                                    "\nwhich jupyterhub-singleuser " +\
                                    "\njupyterhub-singleuser ")
            #script = script.replace('--notebook-dir="/home/kortass/JUPYTER/NOTEBOOKS"','')
            

        os.system("env > %s/jobs/%s_last_script_env" %  (kslhub_root,self.user.name))

        
        f = open("%s/jobs/%s_last_script_modified" % (kslhub_root,self.user.name),"w")
        f.write(script)
        f.close()


        self.log.info('Job content: \n' + '='*80 + '\n' + script + '\n' + '='*80 + '\n')
        
        # self.log.info('Spawner modified script:\n' + script)
        #SKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKkkk
        print("[AUTHENT] in submit_batch_script user: %s or |||%s|| ot type %s " %\
                  (self.user,pprint.pformat(self.user),type(self.user)))

        user = self.user
        user_str = ("%s" % user)
        if user_str.find('<User(')>-1:
            user = user_str[6:].split(' ')[0]



            
        out = yield run_command(cmd, input=script, env=self.get_env(), user=user)
        try:
            self.log.info('Job submitted. cmd: ' + cmd + ' output: ' + out)
            self.job_id = self.parse_job_id(out)
            f = open("%s/jobs/%s_%s.job" % (kslhub_root,self.user.name,self.job_id),"w")
            f.write(script)
            f.close()
            
        except:
            self.log.error('Job submission failed with exit code %s ' % out)
            self.job_id = ''
        return self.job_id

    # Override if your batch system needs something more elaborate to read the job status
    batch_query_cmd = Unicode('', config=True, \
        help="Command to run to read job status. Formatted using req_xyz traits as {xyz} "
             "and self.job_id as {job_id}."
        )

    @gen.coroutine
    def read_job_state(self):
        if self.job_id is None or len(self.job_id) == 0:
            # job not running
            self.job_status = ''
            return self.job_status
        subvars = self.get_req_subvars()
        subvars['job_id'] = self.job_id
        cmd = self.batch_query_cmd.format(**subvars)
        self.log.debug('Spawner querying job: ' + cmd)
        try:
            user = self.user
            user_str = ("%s" % user)
            if user_str.find('<User(')>-1:
                user = user_str[6:].split(' ')[0]
            out = yield run_command(cmd,user=user)
            self.job_status = out
        except Exception as e:
            self.log.error('Error querying job ' + self.job_id)
            self.job_status = ''
        finally:
            return self.job_status

    batch_cancel_cmd = Unicode('', config=True,
        help="Command to stop/cancel a previously submitted job. Formatted like batch_query_cmd."
        )

    @gen.coroutine
    def cancel_batch_job(self):
        subvars = self.get_req_subvars()
        subvars['job_id'] = self.job_id
        cmd = self.batch_cancel_cmd.format(**subvars)
        self.log.info('Cancelling job ' + self.job_id + ': ' + cmd)
        user = self.user
        user_str = ("%s" % user)
        if user_str.find('<User(')>-1:
            user = user_str[6:].split(' ')[0]
        yield run_command(cmd,user=user)

    def load_state(self, state):
        """load job_id from state"""
        super(BatchSpawnerBase, self).load_state(state)
        self.job_id = state.get('job_id', '')
        self.job_status = state.get('job_status', '')

    def get_state(self):
        """add job_id to state"""
        state = super(BatchSpawnerBase, self).get_state()
        if self.job_id:
            state['job_id'] = self.job_id
        if self.job_status:
            state['job_status'] = self.job_status
        return state

    def clear_state(self):
        """clear job_id state"""
        super(BatchSpawnerBase, self).clear_state()
        self.job_id = ""
        self.job_status = ''

    def make_preexec_fn(self, name):
        """make preexec fn to change uid (if running as root) before job submission"""
        return set_user_setuid(name)

    def state_ispending(self):
        "Return boolean indicating if job is still waiting to run, likely by parsing self.job_status"
        raise NotImplementedError("Subclass must provide implementation")

    def state_isrunning(self):
        "Return boolean indicating if job is running, likely by parsing self.job_status"
        raise NotImplementedError("Subclass must provide implementation")

    def state_gethost(self):
        "Return string, hostname or addr of running job, likely by parsing self.job_status"
        raise NotImplementedError("Subclass must provide implementation")

    @gen.coroutine
    def poll(self):
        """Poll the process"""
        if self.job_id is not None and len(self.job_id) > 0:
            yield self.read_job_state()
            if self.state_isrunning() or self.state_ispending():
                return None
            else:
                self.clear_state()
                return 1

        if not self.job_id:
            # no job id means it's not running
            self.clear_state()
            return 1

    startup_poll_interval = Float(5, config=True, \
        help="Polling interval (seconds) to check job state during startup"
        )

    @gen.coroutine
    def start(self):
        """Start the process"""
        if not self.user.server.port:
            self.user.server.port = random_port()
            self.db.commit()
        job = yield self.submit_batch_script()

        # We are called with a timeout, and if the timeout expires this function will
        # be interrupted at the next yield, and self.stop() will be called. 
        # So this function should not return unless successful, and if unsuccessful
        # should either raise and Exception or loop forever.
        assert len(self.job_id) > 0
        while True:
            yield self.poll()
            if self.state_isrunning():
                break
            else:
                if self.state_ispending():
                    self.log.debug('Job ' + self.job_id + ' still pending')
                else:
                    self.log.warn('Job ' + self.job_id + ' neither pending nor running.\n' +
                        self.job_status)
                assert self.state_ispending()
            yield gen.sleep(self.startup_poll_interval)

        self.user.server.ip = self.state_gethost()
        self.db.commit()
        self.log.info("Notebook server job {0} started at {1}:{2}".format(
                        self.job_id, self.user.server.ip, self.user.server.port)
            )

        return self.user.server.ip, self.user.server.port

    @gen.coroutine
    def stop(self, now=False):
        """Stop the singleuser server job.

        Returns immediately after sending job cancellation command if now=True, otherwise
        tries to confirm that job is no longer running."""

        self.log.info("Stopping server job " + self.job_id)
        yield self.cancel_batch_job()
        if now:
            return
        for i in range(10):
            yield self.poll()
            if not self.state_isrunning():
                return
            yield gen.sleep(1.0)
        if self.job_id:
            self.log.warn("Notebook server job {0} at {1}:{2} possibly failed to terminate".format(
                             self.job_id, self.user.server.ip, self.user.server.port)
                )


class BatchSpawnerRegexStates(BatchSpawnerBase):
    """Subclass of BatchSpawnerBase that uses config-supplied regular expressions
    to interact with batch submission system state. Provides implementations of
        state_ispending
        state_isrunning
        state_gethost

    In their place, the user should supply the following configuration:
        state_pending_re - regex that matches job_status if job is waiting to run
        state_running_re - regex that matches job_status if job is running
        state_exechost_re - regex with at least one capture group that extracts
                            execution host from job_status
        state_exechost_exp - if empty, notebook IP will be set to the contents of the
            first capture group. If this variable is set, the match object
            will be expanded using this string to obtain the notebook IP.
            See Python docs: re.match.expand
    """
    state_pending_re = Unicode('', config=True,
        help="Regex that matches job_status if job is waiting to run")
    state_running_re = Unicode('', config=True,
        help="Regex that matches job_status if job is running")
    state_exechost_re = Unicode('', config=True,
        help="Regex with at least one capture group that extracts "
             "the execution host from job_status output")
    state_exechost_exp = Unicode('', config=True,
        help="""If empty, notebook IP will be set to the contents of the first capture group.

        If this variable is set, the match object will be expanded using this string
        to obtain the notebook IP.
        See Python docs: re.match.expand""")

    def state_ispending(self):
        assert self.state_pending_re
        if self.job_status and re.search(self.state_pending_re, self.job_status):
            return True
        else: return False

    def state_isrunning(self):
        assert self.state_running_re
        self.log.info("is_running job_status=/%s/ is_running =/%s/" % \
                      (self.job_status,re.search(self.state_running_re, self.job_status)))

        if self.job_status and re.search(self.state_running_re, self.job_status):
            return True
        else: return False

    def state_gethost(self):
        assert self.state_exechost_re
        match = re.search(self.state_exechost_re, self.job_status)
        self.log.info("is_host job_status=/%s/ host =/%s/" % (self.job_status,match.groups()[0]))

        if not match:
            self.log.error("Spawner unable to match host addr in job status: " + self.job_status)
            return
        if not self.state_exechost_exp:
            return match.groups()[0].replace('sam-1','localhost')
        else:
            return match.expand(self.state_exechost_exp)

class UserEnvMixin:
    """Mixin class that computes values for USER, SHELL and HOME in the environment passed to
    the job submission subprocess in case the batch system needs these for the batch script."""

    def user_env(self, env):
        """get user environment"""
        env['USER'] = self.user.name
        home = pwd.getpwnam(self.user.name).pw_dir
        shell = pwd.getpwnam(self.user.name).pw_shell
        if home:
            env['HOME'] = home
        if shell:
            env['SHELL'] = shell
        return env

    def get_env(self):
        """Add user environment variables"""
        env = super().get_env()
        env = self.user_env(env)
        return env

class SlurmSpawner(UserEnvMixin,BatchSpawnerRegexStates):
    """A Spawner that just uses Popen to start local processes."""

    # all these req_foo traits will be available as substvars for templated strings
    req_partition = Unicode('', config=True, \
        help="Partition name to submit job to resource manager"
        )

    req_qos = Unicode('', config=True, \
        help="QoS name to submit job to resource manager"
        )

    batch_script = Unicode("""#!/bin/bash
#SBATCH --partition={partition}
#SBATCH --time={runtime}
#SBATCH --output={homedir}/jupyterhub_slurmspawner_%j.log
#SBATCH --job-name=spawner-jupyterhub
#SBATCH --workdir={homedir}
#SBATCH --mem={memory}
#SBATCH --export={keepvars}
#SBATCH --uid={username}
#SBATCH --get-user-env=L
#SBATCH {options}

which jupyterhub-singleuser
{cmd}
""",
        config=True)

    if slurm_machine.machine == "locxalhost":
        # outputs line like "Submitted batch job 209"
        batch_submit_cmd = Unicode('/home/kortass/opt/slurm/bin/sbatch', config=True)    
        # outputs status and exec node like "RUNNING hostname"
        batch_query_cmd = Unicode('/home/kortass/opt/slurm/bin/squeue -h -j {job_id} -o "%T %B"', config=True) #
        batch_cancel_cmd = Unicode('/home/kortass/opt/slurm/bin/scancel {job_id}', config=True)

    else:
        batch_submit_cmd = Unicode('sbatch', config=True)
        batch_query_cmd = Unicode('squeue -h -j {job_id} -o "%T %B"', config=True) 
        batch_cancel_cmd = Unicode('scancel {job_id}', config=True)
    

    # use long-form states: PENDING,  CONFIGURING = pending
    #  RUNNING,  COMPLETING = running
    state_pending_re = Unicode(r'^(?:PENDING|CONFIGURING)', config=True)
    state_running_re = Unicode(r'^(?:RUNNING|COMPLETING)', config=True)
    state_exechost_re = Unicode(r'\s+((?:[\w_-]+\.?)+)$', config=True)

    
    def parse_job_id(self, output):
        # make sure jobid is really a number
        try:
            id = output.split(' ')[-1]
            int(id)
        except Exception as e:
            self.log.error("SlurmSpawner unable to parse job ID from text: " + output)
            raise e
        return id

class MultiSlurmSpawner(SlurmSpawner):
    '''When slurm has been compiled with --enable-multiple-slurmd, the
       administrator sets the name of the slurmd instance via the slurmd -N
       option. This node name is usually different from the hostname and may
       not be resolvable by JupyterHub. Here we enable the administrator to
       map the node names onto the real hostnames via a traitlet.'''
    daemon_resolver = Dict({}, config=True, help="Map node names to hostnames")

    def state_gethost(self):
        host = SlurmSpawner.state_gethost(self)
        return self.daemon_resolver.get(host, host)

# vim: set ai expandtab softtabstop=4:
