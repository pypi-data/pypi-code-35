from pyeh.node import Node
import json
import requests
import time
from requests.auth import HTTPBasicAuth

domain = '.elastichosts.com'

class Client:
  def __init__(self, zone, user, pwd, debug=False):
    self.debug = debug
    self.req = Request(zone, user, pwd, debug=debug)

  def log(self, msg):
    if self.debug:
      print(msg)

  def create_node(self, nodeparams):
    # Create node (a 'container' or 'vm')
    try:
      # Get disk for distro
      disk_img = self.get_disk_for_distro(nodeparams.distro, nodeparams.type)
    except Exception as e:
      raise Exception('No disk for distro {}'.format(nodeparams.distro))

    # Create disk, and sync distro to it
    nodeparams.disk = self.clone_disk(disk_img, nodeparams)
    while self.is_cloning(nodeparams.disk, nodeparams.type):
      time.sleep(2)

    node = Node(nodeparams)
    data = node.build_node_json()
    return self.req.post('/servers/create', data)

  def clone_disk(self, disk_img, nodeparams):
    # Returns disk id
    disk_data = { 'name': nodeparams.name }
    if nodeparams.type is 'vm':
      disk_data['size'] = nodeparams.size
      url = '/drives/{}/clone/gunzip'.format(disk_img)
    else:
      url = '/folders/{}/clone'.format(disk_img)
    disk = self.req.post(url, disk_data)
    if nodeparams.type is 'vm':
      return disk['drive']
    else:
      return disk['folder']

  def get_disk_for_distro(self, distro, app_type):
    # Return uuid of distro's disk image
    #   app_type: 'vm', 'container'
    #   distro: e.g. 'debian9'
    self.log('Get image for {}'.format(distro))
    if app_type is 'vm':
      url = '/drives/info/standard'
    else:
      url = '/folders/info/standard'
    try:
      l = self.req.get(url)
    except Exception as e:
      raise Exception('Could not get standard disks')

    for i in l:
      if i['name'].startswith('Debian 9'):
        if app_type is 'vm':
          return i['drive']
        else:
          return i['folder']
    # /for
    raise Exception('Could not find distro')

  def get_servers(self):
    return self.req.get('/servers/list')

  def is_cloning(self, uuid, app_type):
    # Given uuid of a disk, return True if the disk is cloning
    # app_type = 'vm' or 'container'
    if app_type is 'vm':
      if 'imaging' in self.req.get('/drives/{}/info'.format(uuid)).keys():
        return True
    else:
      if 'syncing' in self.req.get('/folders/{}/info'.format(uuid)).keys():
        return True
    return False

class Request:
  def __init__(self, zone, user, pwd, debug=False):
    self.url = 'https://api.' + zone + domain
    self.auth = HTTPBasicAuth(user, pwd)
    self.debug = debug

  def log(self, msg):
    if self.debug:
      print(msg)

  # PRIVATE
  # HTTP REST wrappers
  def get(self, url):
    return self.request('GET', url)

  def post(self, url, data):
    return self.request('POST', url, data)

  # Request
  def request(self, method, url, data=None):
    url = self.url + url
    self.log('{} {}'.format(method, url))
    headers = {'Accept': 'application/json'}
    try:
      if method == 'POST' and data != None:
        self.log('DATA')
        self.log(json.dumps(data, indent=2))
        f = requests.post(url, auth=self.auth, headers=headers, json=data)
      else:
        f = requests.get(url, auth=self.auth, headers=headers)
      f.raise_for_status()
      return json.loads(f.text)
    except requests.exceptions.HTTPError as e:
      print('%s' %e)
      raise e
    except requests.exceptions.RequestException as e:
      print('Other error: %s' %e)
