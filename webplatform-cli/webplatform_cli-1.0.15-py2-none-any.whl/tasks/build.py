from webplatform_cli.lib.config import Settings
from docker import APIClient
import os

def build_base(service, path, force):
   settings = Settings()
   client = APIClient(base_url="unix://var/run/docker.sock")

   name = "webplatform-base-%s" % service
   image_name = 'webplatform-base-%s:latest' % (service)

   print("Building base image for (%s)." % service)
   kwargs = {
      'decode': True,
      # 'nocache': force,
      'forcerm': True,
      'path': path,
      'rm': True,
      'tag': image_name,
      'stream': True,
      # 'container_limits': {
      #    'cpusetcpus': '0-4',
      #    'memory': 1073741824,
      # }
   }
   for line in client.build(**kwargs):
      if "stream" in line: print(line['stream'])
   print("Done -- building base image for (%s)." % service)

def run(service, path, context=None, force=False, base=True):
   image_name = 'webplatform-%s:latest' % service

   if base:
      build_base(service.split("_")[0], base, force)

   dockerfile = path + 'Dockerfile'
   if not context:
      context = path

   print("Building (%s) image." % service)
   kwargs = {
      'nocache': force,
      'decode': True,
      'forcerm': True,
      'path': context,
      'dockerfile': dockerfile,
      'rm': True,
      'tag': image_name,
      # 'container_limits': {
      #    'cpusetcpus': '0-4',
      #    'memory': 1073741824,
      # }
   }
   for line in client.build(**kwargs):
      if "stream" in line: print(line['stream'])
   print("Done -- building base image for (%s)." % service)
