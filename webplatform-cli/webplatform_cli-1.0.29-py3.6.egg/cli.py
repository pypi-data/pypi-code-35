from handler import ContainerHandler
import os, docker

class Docker(object):
   def __init__(self, settings, debug, force):
      self.settings = settings
      self.config = self.settings.get_config("cli")
      self.debug = debug
      self.force = force

      self.options = {
         "debug": self.debug,
         "force": self.force,
      }

      self.client = docker.DockerClient(base_url="unix://var/run/docker.sock")
      self.services = self.settings.get_service()
      self.base_path = settings.get_path()

   def parse_args(self, **kwargs):
      #only run setup and install, others have yet to be implemented
      if kwargs['command'] in "setup":
         getattr(self, "%s" % (kwargs['command'], ), None)(kwargs['params'])

      elif kwargs['command'] in ["start", "restart", "stop", "update", "reset"]:

         if len(kwargs['params']) > 0:
            for i in kwargs['params']:
               self.run_container(service=i, action=kwargs['command'])
         else:
            self.run_container(action=kwargs['command'])

      elif kwargs['command'] == "tail":
         self.tail(kwargs['params']['service'], follow=kwargs['params']['follow'])

   def run_container(self, service=None, action=None):
      container = ContainerHandler(self.settings, self.client, self.options)
      if service == None:
         container.run(action)
      else:
         container.run_service(service, action)

   def setup(self, params):
      from tasks import build
      force = self.options['force']

      docker_file = "%s/db/docker/" % self.base_path
      build.run("mongodb", docker_file, force=force, base=False)
