import os
from utils import verifyName
from error import GadgetInvalid

# Gadget Config
# ----
# Gadgets can have multiple configs when in use
# This class handles creating said configs, and maintaining which functions
# are in use by the config
# Parameters:
# name: The name to use for the config.  this must be in the form of 'c.#' to
#       work correctly
class Config:
    def __init__(self,name):
        if not verifyName(name):
            raise GadgetInvalid("Attempted to create a config with an invalid name")
        self.name = name
        self.functions = []
    def write(self,path):
        myPath = os.path.join(path,'configs',self.name)
        existingFunctions = [f for f in os.listdir(myPath) if verifyName(f)]
        for func in existingFunctions:
            if not func in self.functions:
                os.remove(os.path.join(myPath,func))
        for func in self.functions:
            if not os.path.exists(os.path.join(myPath,func)):
                os.symlink(os.path.join(path,'functions',func),os.path.join(myPath,func))
    def buildPath(self,path):
        configPath = os.path.join(path,self.name)
        os.mkdir(configPath)
    # NOTE: This does not currently verify if the function is part of the correct
    #       gadget.  Wierd things may happen if you try to cross gadgets
    def addFunction(self,function):
        self.functions.append(function.name)
        pass
