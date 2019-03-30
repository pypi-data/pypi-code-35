import os

from error import GadgetInvalid
from .utils import verifyName

# Gadget Function 
# ----
# Gadgets can have multiple functions per config
# This class defines the basic function type.
# Please note that this class doesn't implement any
# function features or type, and so can't be directly implemented
# Parameters: 
# name: Name of the function device.  This doesn't include the type,
#       and must be formated as "<name>#". E.g. "usb0"
class Function:
    def __init__(self,name):
        if not self.type:
            raise GadgetInvalid("Attempted to create a raw function element")
        self.name = self.type+"."+name
        if not verifyName(self.name):
            raise GadgetInvalid("Attempted to create a function with an invalid name")
    def write(self,path):
        pass
    def buildPath(self,path):
        functionPath = os.path.join(path,self.name)
        os.mkdir(functionPath)

# Mass Storage Function
# ----
# Implementation of the Mass Storage Function
# Can handle passing a single file as a mass storage partition
# Currently doesn't implement any support for additional luns, but will auto
# create the first one.
# Parameters:
# No additional parameters from Function
class MassStorage(Function):
    def __init__(self,name):
        self.type="mass_storage"
        Function.__init__(self,name)
        self.cdrom = False
        self.readOnly = False
        self.image = ""
        self.nofua = False
        self.removable = False
    def write(self,path):
        # NOTE: Cant write to the file using open, so we are using os.system.  Need to see what is needed
        # to fix this.
        lunPath = os.path.join(path,'lun.0')
        os.system('echo "%s" > %s' % (self.image, os.path.join(lunPath,'file')))
        if self.cdrom:
            os.system('echo "1" > %s' % os.path.join(lunPath,'cdrom'))
        else:
            os.system('echo "0" > %s' % os.path.join(lunPath,'cdrom'))
        if self.readOnly:
            os.system('echo "1" > %s' % os.path.join(lunPath,'ro'))
        else:
            os.system('echo "0" > %s' % os.path.join(lunPath,'ro'))
        if self.nofua:
            os.system('echo "1" > %s' % os.path.join(lunPath,'nofua'))
        else:
            os.system('echo "0" > %s' % os.path.join(lunPath,'nofua'))
        if self.removable:
            os.system('echo "1" > %s' % os.path.join(lunPath,'removable'))
        else:
            os.system('echo "0" > %s' % os.path.join(lunPath,'removable'))
