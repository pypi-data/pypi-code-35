import os
import subprocess
from getpass import getpass

import json
from .bitbucket import BitBucketApi
from .utils import Clr, Utils


class Config:
    def __init__(self):
        pass

    HOME = os.getenv('HOME')
    SYS_CONFIG_FILE = os.path.join(HOME, '.oly', 'config.json')
    SERVICES_DIR = os.path.basename(os.path.join(Utils.ROOT_DIR, 'services'))
    TOOLS_DIR = os.path.join(HOME, '.oly', 'tools')

    def get_sys_config(self):
        if not self.sys_config_exists():
            return None

        with open(self.SYS_CONFIG_FILE) as f:
            if os.stat(self.SYS_CONFIG_FILE).st_size == 0:
                return None

            data = json.load(f)
            return data

    def get_tools(self):
        if self.get_sys_config():
            return self.get_sys_config()['tools']
        return

    def get_available_tools(self):
        return self.get_tools()

    def update_sys_config(self, config):
        config_file = open(self.SYS_CONFIG_FILE, 'w')
        json.dump(config, config_file, default_flow_style=False)
        return

    def sys_config_exists(self):
        if not os.path.isfile(self.SYS_CONFIG_FILE):
            return False
        return True


class SysConfig:
    def __init__(self):
        pass

    conf = Config().SYS_CONFIG_FILE

    def setup(self, no_interaction=False):
        sys_conf = Config().get_sys_config()
        config = {
            "bit-bucket": {
                "username": "",
                "password": "",
                'owner': 'paperclicks'
            },
            "rancher": {
                "accessKey": "",
                "secretKey": "",
                "url": "",
            },
            "docker-hub": {},
            "jenkins": {},
            "tools": ["mysql", "postgres", "mongo", "rabbitmq", "redis", "swagger"]
        }

        config_file = open(self.conf, 'w')

        # Clr('Press enter on each question to skip or run config with --no-interaction option').ok()
        Clr('Press enter to skip...').ok()

        if no_interaction is False:
            bb = self.set_bit_bucket_credentials(sys_conf)
            config['bit-bucket'] = bb

        json.dump(config, config_file, sort_keys=True, indent=4)
        # self.setup_network()
        print('')
        Clr('Setup finished successfully!').ok_banner()
        print('')

    @staticmethod
    def dump_config(no_security=False):
        sys_conf = Config().get_sys_config()

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
    def get_bit_bucket_username():
        sys_c = Config().get_sys_config()
        if sys_c:
            return sys_c['bit-bucket']['username']
        return ''

    @staticmethod
    def get_bit_bucket_pass():
        sys_c = Config().get_sys_config()
        if sys_c:
            return sys_c['bit-bucket']['password']
        return ''

    @staticmethod
    def get_bit_bucket_owner():
        sys_c = Config().get_sys_config()
        if sys_c:
            return sys_c['bit-bucket']['owner']
        return ''

    @staticmethod
    def set_bit_bucket_credentials(sys_conf=None):
        credentials = {
            'username': '',
            'password': '',
            'owner': 'paperclicks'
        }

        if sys_conf:
            credentials['username'] = sys_conf['bit-bucket']['username']
            credentials['password'] = sys_conf['bit-bucket']['password']
            credentials['owner'] = sys_conf['bit-bucket']['owner']

        bb_owner = Utils.m_input(
            'BitBucket owner ' + Clr.WARNING + '[' + credentials['owner'] + ']' + Clr.RESET + ': ')
        bb_user = Utils.m_input(
            'BitBucket username ' + Clr.WARNING + '[' + credentials['username'] + ']' + Clr.RESET + ': ')

        if bb_user:
            credentials['username'] = str(bb_user)

        if not bb_owner:
            credentials['owner'] = 'paperclicks'
        else:
            credentials['owner'] = str(bb_owner)

        bb_pass = getpass('BitBucket password ' + Clr.WARNING + '[' + Utils.cli_obfuscate(credentials['password']) + ']' + Clr.RESET + ': ')

        if bb_pass:
            credentials['password'] = str(bb_pass)

        # validate bit-bucket credentials
        if credentials['username'] and credentials['password']:
            bb = BitBucketApi(credentials['username'], credentials['password'])
            if bb.get_user() is None:
                Clr('Invalid BitBucket credentials.').error()
            else:
                Clr('- BitBucket credentials OK.').ok()

        return credentials

    @staticmethod
    def setup_network():
        net = Utils.NETWORK
        print("\nCreating " + net + " network...")
        cmd = """
            if [[ $(docker network ls -f name=olynet | grep olynet | awk '{print $2}') != 'olynet' ]]; then
                create_cmd=$(docker network create olynet | awk '{print $1}')
                if [[ ${create_cmd} ]]; then
                    echo -e "\033[92mOK\033[0m"
                fi
            else
                echo -e "\033[92mOK\033[0m"
            fi
        """
        subprocess.check_output(cmd, shell=True)



























