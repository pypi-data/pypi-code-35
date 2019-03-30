import os

from utils import verifyPointer
from error import GadgetExists, GadgetMounted, PointerMounted

# USB Gadget Class
# ----
# Manages a single usb gadget for usage on things like RPi Zero
# Parameters:
# name: Name of the gadget.  this is what goes into the usb_gadget folder.
# path: Path to the usb_gadget folder.  Under /sys/kernel/config/ by default in Raspbian, but can be changed
#       by mounting cfgfs somewhere else.
# write: Defaults to True. Whether or not to immediatly create the gadget folder when initializing the gadget.

class Gadget:
    def __init__(self,name,path,write=True):
        self.idVendor = "0x1d6b"
        self.idProduct = "0x0104"
        self.bcdDevice = "0x0100"
        self.bcdUSB = "0x0200"
        self.serialnumber="fedcba9876543210"
        self.manufacturer="Lorium Ipsum"
        self.product="Python Gadget"
        self.name = name
        self.path = os.path.join(path,name)
        self.configs = {}
        self.functions = {}
        stringsPath = os.path.join('strings','0x409')
        self.files = {
                'idVendor': 'idVendor',
                'idProduct': 'idProduct',
                'bcdDevice': 'bcdDevice',
                'bcdUSB': 'bcdUSB',
                os.path.join(stringsPath,'manufacturer'):'manufacturer',
                os.path.join(stringsPath,'serialnumber'):'serialnumber',
                os.path.join(stringsPath,'product'):'product',
        }
        if self.exists():
            raise GadgetExists()
        if write:
            self.buildPaths()
            self.write()
    def exists(self):
        return os.path.isdir(self.path)
    def isMounted(self):
        UDCPath = os.path.join(self.path,'UDC')
        with open(UDCPath,'r') as f:
            content = f.read()
            return len(content.strip()) > 0
    # Write out gadget data
    # Should be called when you set or update any of the gadget, function, or config info
    # Will throw an error if the gadget is currenty enabled
    def write(self):
        if self.isMounted():
            raise GadgetMounted()
            return
        for fName,name in self.files.items():
            with open(os.path.join(self.path,fName),'w') as f:
                f.write(self.__dict__[name])
        for name,function in self.functions.items():
            function.write(os.path.join(self.path,'functions',function.name))
        for name,config in self.configs.items():
            config.write(self.path)
    # Build inital paths
    # Should only be called once to generate the inital paths.
    def buildPaths(self):
        if self.exists():
            raise GadgetExists()
        os.mkdir(self.path)
        # NOTE: 0x409 is for English.  Should eventually add support for other languages at
        # some point
        stringsPath = os.path.join(self.path,'strings')
        englishPath = os.path.join(self.path,'strings','0x409')
        if not os.path.exists(stringsPath):
            os.mkdir(stringsPath)
        if not os.path.exists(englishPath):
            os.mkdir(englishPath)
    # Will attempt to bind the gadget to a usb pointer.  Will first check to see if the pointer
    # exists, then verify that it is currently not in use.
    def activate(self,pointer):
        if not verifyPointer(self.path,pointer):
            raise PointerMounted()
        os.system('echo "%s" > %s' % (pointer, os.path.join(self.path,'UDC')))
    def deactivate(self):
        os.system('echo "" > %s' % os.path.join(self.path,'UDC'))
    # Add a config to the gadget
    def addConfig(self,config):
        self.configs[config.name] = config
        config.buildPath(os.path.join(self.path,'configs'))
    # Add a function to the gadget
    def addFunction(self,function):
        self.functions[function.name] = function
        function.buildPath(os.path.join(self.path,'functions'))
