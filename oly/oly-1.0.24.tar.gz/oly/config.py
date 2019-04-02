import os
import shutil
import json
import pkg_resources

from getpass import getpass
from .bitbucket import BitBucketApi
from .utils import Clr, Utils


class Config:
    def __init__(self):
        pass

    def configure(self):
        self._create_oly_home()
        self.install_tools()
        self._create_create_projects_dir()
        config = self.read_config()
        if not config:
            config = self._config_mock()
        bb = self.set_bit_bucket_credentials(config)
        config['bit-bucket'] = bb
        self.update_config(config)
        print('')
        Clr('Setup finished successfully!').ok_banner()
        print('')

    def read_config(self):
        if not self.config_exists():
            return
        with open(Utils.CONFIG_FILE) as f:
            if os.stat(Utils.CONFIG_FILE).st_size == 0:
                return None

            data = json.load(f)
            return data

    @staticmethod
    def get_tools():
        if not os.path.isdir(Utils.TOOLS_DIR):
            return []
        tools = os.listdir(Utils.TOOLS_DIR)
        if tools:
            for tool in tools:
                if not os.path.isdir(os.path.join(Utils.TOOLS_DIR, tool)):
                    tools.remove(tool)
        return tools

    @staticmethod
    def install_tools(force=False):
        pkg_tools_dir = pkg_resources.resource_filename('oly', 'tools')
        try:
            if not os.path.isdir(Utils.TOOLS_DIR):
                shutil.copytree(pkg_tools_dir, Utils.TOOLS_DIR)
            elif not force and os.path.isdir(Utils.TOOLS_DIR):
                return
            elif force:
                shutil.rmtree(Utils.TOOLS_DIR)
                shutil.copytree(pkg_tools_dir, Utils.TOOLS_DIR)
        except OSError as e:
            msg = e.strerror
            if e.errno == 17:
                msg = 'The tools directory already exist, run "oly config --force-install-tools" to remove and install again'
            Clr('Tools cannot be installed!\n'+ msg).error_banner()
            exit(e.errno)


    @staticmethod
    def update_config(data):
        """Update the config file and returns updated config data"""
        config_file = open(Utils.CONFIG_FILE, 'w')
        json.dump(data, config_file)
        return data

    @staticmethod
    def set_bit_bucket_credentials(config=None):
        credentials = {
            'username': '',
            'password': '',
            'owner': ''
        }

        if config:
            credentials['username'] = config['bit-bucket']['username']
            credentials['password'] = config['bit-bucket']['password']
            credentials['owner'] = config['bit-bucket']['owner']
        try:
            bb_owner = Utils.m_input(
                'BitBucket owner ' + Clr.WARNING + '[' + credentials['owner'] + ']' + Clr.RESET + ': ')
            bb_user = Utils.m_input(
                'BitBucket username ' + Clr.WARNING + '[' + credentials['username'] + ']' + Clr.RESET + ': ')

            if bb_user:
                credentials['username'] = str(bb_user).strip()

            if bb_owner:
                credentials['owner'] = str(bb_owner).strip()

            bb_pass = getpass('BitBucket password ' + Clr.WARNING + '[' + Utils.cli_obfuscate(credentials['password']) + ']' + Clr.RESET + ': ')

            if bb_pass:
                credentials['password'] = str(bb_pass)
        except KeyboardInterrupt:
            print('\n' + Clr.WARNING + 'Aborted!' + Clr.RESET)
            print('')
            exit(0)

        # validate bit-bucket credentials
        if credentials['username'] and credentials['password']:
            bb = BitBucketApi(credentials['username'], credentials['password'])
            if bb.get_user() is None:
                Clr('Invalid BitBucket credentials.').error()
            else:
                Clr('- BitBucket credentials OK.').ok()

        return credentials

    @staticmethod
    def _create_oly_home():
        if not os.path.isdir(Utils.OLY_HOME):
            os.mkdir(Utils.OLY_HOME)

    @staticmethod
    def _create_create_projects_dir():
        if not os.path.isdir(Utils.PROJECTS_DIR):
            os.mkdir(Utils.PROJECTS_DIR)

    def _create_empty_config(self):
        config_file = open(Utils.CONFIG_FILE, 'w')
        json.dump(self._config_mock(), config_file)
        return

    def _config_mock(self):
        config = {
            "bit-bucket": {
                "username": "",
                "password": "",
                'owner': ''
            },
            "rancher": {
                "accessKey": "",
                "secretKey": "",
                "url": "",
            },
            "docker-hub": {},
            "jenkins": {},
            "tools": self.get_tools()
        }
        return config

    def get_bit_bucket_username(self):
        return self.read_config()['bit-bucket']['username']

    def get_bit_bucket_pass(self):
        return self.read_config()['bit-bucket']['password']

    def get_bit_bucket_owner(self):
        return self.read_config()['bit-bucket']['owner']

    @staticmethod
    def dump(no_security=False):
        sys_conf = Config().read_config()
        if sys_conf:
            for root, conf in sys_conf.items():
                if isinstance(conf, dict):
                    if conf:
                        Clr(root + ':').warn()
                        for key, val in conf.items():
                            if not val == '':
                                if (key == 'password' or key == 'pass' or key == 'secret') and (no_security is False):
                                    print("    " + Clr.WARNING + key + ': ' + Clr.RESET + Clr.OK + Utils.cli_obfuscate(val) + Clr.RESET)
                                else:
                                    print("    " + Clr.WARNING + key + ': ' + Clr.RESET + Clr.OK + val + Clr.RESET)
                                # Clr('   ' + key + ': ' + val).ok()
                            else:
                                print("    " + Clr.WARNING + key + ': ' + Clr.RESET + Clr.FAIL + '~' + Clr.RESET)
                                # Clr('   ' + key + ': ~').ok()
                    else:
                        print(Clr.WARNING + root + ': ' + Clr.RESET + Clr.FAIL + '~' + Clr.RESET)
                        # Clr(root + ': ~').warn()

                elif isinstance(conf, list):
                    print(Clr.WARNING + root + ': ' + Clr.RESET + Clr.OK + ', '.join(conf) + Clr.RESET)
            return True

    @staticmethod
    def config_exists():
        if not os.path.isfile(Utils.CONFIG_FILE):
            return False
        return True



























