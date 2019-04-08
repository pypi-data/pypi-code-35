import json

class NodeParams:
  name = None
  type = 'container'
  distro = 'debian9'
  cpusize = 500
  disksize = 10
  memsize = 512
  persistent = False
  disk = None

class Node:
  # TODO: Handle disk size on VM
  def __init__(self, nodeparams):
    self.params = nodeparams
    pass

  def build_node_json(self):
    res = {
      'name': self.params.name,
      'type': self.params.type,
      'mem': self.params.memsize,
      'cpu': self.params.cpusize,
      'nic:0:model': 'e1000',
      'nic:0:dhcp': 'auto',
      'password': 'Tr0l0l0'
    }
    if self.params.type is 'vm':
      res['boot'] = 'ide:0:0'
      res['ide:0:0'] = self.params.disk
      res['vnc'] = 'auto'
    else:
      res['fs:0:mount'] = '/'
      res['fs:0'] = self.params.disk
      if self.params.persistent:
        res['persistent'] = True
    return res
