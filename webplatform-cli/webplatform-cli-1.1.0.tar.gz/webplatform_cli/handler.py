try:
   import simplejson
except:
   import json as simplejson

import collections, imp, time, sys

class ContainerHandler:
   def __init__(self, settings, client, options=dict()):
      self.settings = settings

      if "debug" in list(options.keys()):
         self.debug = options.get("debug")
      else:
         self.debug = False

      if "force" in list(options.keys()):
         self.force = options.get("force")
      else:
         self.force = False

      self.services = self.settings.get_service()
      self.client = client

   def run(self, action):
      run = getattr(self, action, None)
      if run != None and isinstance(run, collections.Callable):
         run()
      elif action in ["start", "stop", "restart"]:
         for service in self.services:
            self.run_service(service, action)

   def run_service(self, service, action):
      check = self.check_running(service)
      if type(check) is list:
         for check_container in check:
            container = self.__eval_container(check_container['container'], service, action, node=check_container['node'])

            service_name = "%s_%s" % (service, check_container['node'])
            if container and "exited" in container.status and action != "stop":
               print("Service ('%s') has encounter an error, either rebuild the container or start the container using the '-f' |'--force' flag." % service_name)

      else:
         container = self.__eval_container(check, service, action)
         service_name = service
         if container and "exited" in container.status and action != "stop":
            print("Service ('%s') has encounter an error, either rebuild the container or start the container using the '-f' |'--force' flag." % service_name)

   def __eval_container(self, container, service, action, node=False):
      service_name = service
      if node:
         service_name = "%s_%s" % (service, node)

      running = False
      error = False
      has_script = False

      if container and "exited" in container.status and action == "stop":
         print("Service '%s' is already stopped." % service_name)
         sys.exit()

      elif container and ("running" in container.status or "created" in container.status):
         running = True

      elif container and (not "exited" in container.status and not "" in container.status):
         running = True

      if self.force and action == "reset":
         if not container:
            print("You can only 'reset' a container if the container is currently running.\nStart the container and rerun the 'reset' command.")
            sys.exit()

         print("Preforming a 'reset'. Removing and Restart Container.\n")
         print("Stopping '%s' container." % service)
         container.stop()
         print("Removing '%s' container." % service)
         container.remove()

         print("Creating '%s' container" % service)
         container = self.create_container(service, node=node)
         print("Starting '%s' container.\n\nFinished 'reset'" % service)
         container.start()
         sys.exit()

      if action == 'reset':
         print("Preforming a 'hard-reset' will remove the container and start it again.")
         print("If you are sure you want to preform this action pass the '-f' option")
         sys.exit()

      if action == "start":
         if not running and not container:
            print("Creating '%s' container" % service)
            container = self.create_container(service, node=node)
            print("Starting '%s' container" % service)
            container.start()
            sys.exit()

         elif not running and container:
            print("Starting '%s' container" % service)
            container.start()
            sys.exit()

         elif running and container:
            print("Container '%s' is already running. Checking for 'start' script." % service)

         new_action = self.settings.get_actions(service)
         if not new_action[action]['default']:
            has_script = True

      elif action == 'restart':
         if running and self.force:
            print("Restarting '%s' container" % service)
            container.restart()
            sys.exit()

         elif running and not self.force:
            print("Checking for 'restart' script on '%s' container" % service)
            new_action = self.settings.get_actions(service)

            if not new_action[action]['default']:
               has_script = True

         else:
            print("Container '%s' is current stopped. Starting container." % service)
            container.start()
            sys.exit()

      elif action == 'stop':
         if running and self.force:
            print("Stopping '%s' container" % service)
            container.stop()
            sys.exit()

         else:
            new_action = self.settings.get_actions(service)
            if not new_action[action]['default']:
               has_script = True

      elif action == "update" and running:
         new_action = self.settings.get_actions(service)
         if not new_action[action]['default']:
            has_script = True
         else:
            print("Service doesn't have an update action.")
            sys.exit()

      if has_script:
         print("Found '%s' script for '%s' container.\nContainer output.\n" % (action, service))

         cmd = '%s %s' % new_action[action]['cmd']
         output = container.exec_run(cmd, stream=True)

         try:
            for line in output:
               print(line.decode("utf-8")[:-1])

            print("\nFinished excuting '%s' action on '%s'" % (action, service))
         except KeyboardInterrupt:
            sys.exit()

      else:
         print("Container '%s' has no '%s' script." % (service, action))
         print("Preforming normal '%s' on '%s' container normally." % (action, service))

         getattr(container, action)()
         sys.exit()


      return container

   def create_network(self):
      network = self.client.networks.create(name="webplatform")
      return network

   def create_container(self, service, node=False):
      base_path = self.settings.get_path()

      service = service.replace("-", "_")
      service_name = service
      if node:
         service_name = "%s_%s" % (service, node)

      network = self.check_network()
      if network == None:
         network = self.create_network()

      settings = self.settings.get_config(service)

      if node:
         settings = settings[node]

      container = imp.load_source(service, settings['container'])
      return container.create(self.client, network)

   def check_running(self, service):
      services = self.settings.get_service(service=service)

      if type(services) is list:
         containers = []
         for i in services:
            found = False
            name = "webplatform-%s_%s" % (service, i)
            for container in self.client.containers.list(all=True):
               if name in container.name:
                  containers.append({'container': container, 'node': i})
                  found = True

            if not found:
               containers.append({'container': False, 'node': i})

         return containers

      else:
         name = "webplatform-%s" % service
         for container in self.client.containers.list(all=True):
            if name in container.name:
               return container
         return False

   def check_network(self):
      name = "webplatform"
      for network in self.client.networks.list():
         if name in network.name:
            return network
      return None
