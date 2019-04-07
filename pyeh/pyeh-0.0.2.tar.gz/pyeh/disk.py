import json

class DiskParams:
  name = None
  distro = 'debian9'
  size = None

class Disk:
  def __init__(self, nodeparams):
    self.params = nodeparams
    pass

  def build_disk_json(self):
    diskid = '3dccaad6-e2d5-4aa9-9974-77cea9c01ad5'
    if self.params.type is 'vm':
      disk_key = 'ide:0:0'
      extra_key = 'boot'
      extra_val = 'ide:0:0'
    else:
      disk_key = 'fs:0'
      extra_key = 'fs:0:mount'
      extra_val = '/'

    res = {
      'name': self.params.name,
      'type': self.params.type,
      'mem': self.params.memsize,
      'cpu': self.params.cpusize,
      disk_key: self.params.diskid,
      extra_key: extra_val,
      'nic:0:model': 'e1000',
      'nic:0:dhcp': 'auto',
      'persistent': 'true',
      'vnc': 'auto',
      'password': 'Tr0l0l0'
    }
    return res
