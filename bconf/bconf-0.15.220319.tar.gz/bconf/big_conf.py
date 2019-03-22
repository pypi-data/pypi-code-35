## CONFIG MANAGER ##
## BIG_CONF ##

# Standard Imports
import os

class bconf:

    # Constructor
    def __init__(self, file_path="def.bconf", delim="="):
        '''Creates a new config manager with the specified settings then attempts to read/create the config
        file at the current file path.'''

        if not file_path:
            raise Exception("Cannot have an empty file path location.")
        
        self.file_path = file_path
        self.set_delim(delim)
        self.config = {}
        self.read_conf()            

    # Create the config file if it doesn't already exist
    def create_config_file(self, file_path=None):
        '''If the config file does not exist, a new one is created.'''
        fp = file_path if file_path else self.file_path
        
        if not os.path.isfile(fp):
            try:
                conf = open(fp, "w").close()
            except Exception as exc:
                raise Exception("Cannot write to the specified file path: {}".format(fp))     

    # Write the current config to the file path
    def write_conf(self, file_path=None):
        '''Writes the running config to the config manager's file path.'''
        fp = file_path if file_path else self.file_path

        try:
            f = open(fp, "w")
            f.write(''.join(str(k + self.delim + v + "\n") for k,v in self.config.items())) 
            f.close()
        except Exception as exc:
            raise Exception("Cannot write to the specified file path: {}".format(fp))

    # Read in the config from the specified file
    def read_conf(self, file_path=None):
        '''Reads in a config file from the current config manager's file path. Will also check if it
        exists and create it if not.'''
        fp = file_path if file_path else self.file_path
        
        self.create_config_file() # Check file exists
        try: 
            self.config = {param.split(self.delim)[0]: param.split(self.delim)[1].rstrip() for param in open(self.file_path, "r")}
        except IndexError:
            print("Error: Config format is incorrect!")

    # Add a parameter to the running config
    def add_params(self, params={}):
        '''Takes a dictionary of parameters (key/value pairs) and adds them to the running config.
        Passing already existing keys will update the value.'''
        try:
            for k,v in params.items():
                self.config[k] = v
        except AttributeError as err:
            raise AttributeError("add_params() is expecting a dictionary as a parameter. Input was of type: {}".format(type(params)))
            

    # Remove a parameter from the running config
    def remove_params(self, params=[]):
        '''Takes a list of parameter keys to be removed from the running config.'''
        for param in params:
            try:
                del self.config[param]
            except:
                print("Error: Key '{}' does not exist in the running config!".format(param))

    # Change the default delimiter
    def set_delim(self, delim="="):
        '''Sets the delimiter to be used on the config file read/write.'''
        self.delim = delim

    # Change the running config path
    def set_file_path(self, path, load=False):
        '''Changes the file path for all read/write operations. A second 
        parameter of boolean value can be provided to indicate whether to read
        from the new directory.'''
        self.file_path = path
        if load:
            self.read_conf()

    # Get value of a parameter
    def get_value(self, param):
        '''Gets the value of the specified parameter name parameter. Returns
        None when no value is found.'''
        return self.config.get(param)

    # Sets the value of an existing parameter.
    def set_value(self, param, value):
        '''Sets the value of an existing parameter. Returns True on success and 
        False on failure'''
        if self.get_value(param):
            self.config[param] = value
            return True
        else:
            return False

    # Print overload
    def __str__(self):
        message = "Parameters:\n"
        message += (''.join(str(k + " : '" + v + "'\n") for k, v in self.config.items()) if len(self.config) else "None\n") + "\n"
        message += "Settings:\n"
        message += "File Path: {}\n".format(self.file_path)
        message += "Delimiter: '{}'\n".format(self.delim)
        return message
        



if __name__ == "__main__":

    con_man = bconf("test")
    print(con_man)
