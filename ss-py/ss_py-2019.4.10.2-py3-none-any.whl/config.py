from aigpy import configHelper

class SSConfig(object):
    def __init__(self, path):
        self.path    = path
        self.rootDir = configHelper.GetValue('com','rootdir','./',self.path)

    def save(self):
        configHelper.SetValue('com','rootdir',self.rootDir, self.path)