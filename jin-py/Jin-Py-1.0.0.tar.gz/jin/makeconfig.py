import os
import sys

CONFIG_PROPERTIES = {
    "sloc": "host_address",     # Source location
    "sdir": "host_location",    # Source directory
    "dloc": "remote_address",   # Destination location
    "ddir": "remote_location",  # Destination directory
    "wmin": "watch_min_updated",
    "igspec": "ignore_specific",
    "igtype": "ignore_filetype"
}

initialConfig = f"""# This is a standard Jin configuration file
# Uncomment and edit the lines below as needed

# Note: host_address and remote_address are optional if working on a local machine

# Host (source) information
# {CONFIG_PROPERTIES.get("sloc")}: example@xxx.xxx.x.x
# {CONFIG_PROPERTIES.get("sdir")}: /location/inside/source/

# Remote (destination) information
# {CONFIG_PROPERTIES.get("dloc")}: example@xxx.xxx.x.x
# {CONFIG_PROPERTIES.get("ddir")}: /location/inside/destination/

# Minimum amount of files needing to update before pushing
# automatically (only used if 'watch' flag is used)
# {CONFIG_PROPERTIES.get("wmin")}: 5

# Folders, files, and filetypes to ignore
{CONFIG_PROPERTIES.get("igspec")}: .jinconfig
{CONFIG_PROPERTIES.get("igtype")}: *.jin
"""

class Maker:
    """Creates Jin project files"""

    def __init__(self, args):
        self.args = args

    def createNewConfig(self):
        if os.path.isfile("./.jinconfig"):
            print(".jinconfig file already exists! Skipping...")
            sys.exit(1)

        with open(".jinconfig", "w+") as config:
            if config is None:
                print(".jinconfig file couldn't be created! Do you have proper permissions?")
                sys.exit(1)

            config.write(initialConfig)

        try:
            os.makedirs(".jin/_blank/")
        except OSError:
            print("Unable to create .jin directory! Do you have proper permissions or does it already exist?")
            sys.exit(1)

        print(f"A new Jin project has been created in {os.getcwd()}")
