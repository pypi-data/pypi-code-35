from containers import main
import docker, socket

base_path = main.base_path
volumes = main.volumes

service = "mongodb"

settings = main.settings.get_config(service)

name = "webplatform-%s" % service
num_cores = main.settings.get_num_cores(service, get_range=True)

environment = main.get_environment(service)

def create(client, network):
   num_cores = main.settings.get_num_cores(service, get_range=True)

   devel_volumes = {
      "%s/db/docker/" % base_path: {
         "bind": "/home/container/config/",
         "mode": "rw",
      },
      "%s/db/data/%s" % (base_path, service): {
         "bind": "/data/db",
         "mode": "rw",
      },
   }

   print(devel_volumes)
   volumes = main.add_volumes(devel_volumes)
   ports = {
      str(settings['port']): settings['port']
   }
   kwargs = {
      # "image": "mongo:latest",
      "image": "webplatform-%s:latest" % service,
      "name": name,
      "hostname": service,
      "tty": True,
      "ports": ports,
      "mem_limit": "8g",
      "environment": environment,
      "volumes": volumes,
      # "user": "mongodb",
   }

   if num_cores != None:
      kwargs['cpuset_cpus'] = num_cores

   container = client.containers.create(**kwargs)
   network.connect(container, aliases=[service])
   return container
