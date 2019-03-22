
class User():
    def __init__(self, name, role, address, password=None, config_template_path=None, config_path=None):
        """

        :param name: Just to keep track and personalize the simulation
        :param role: Also just for personalizing
        :param address: This the account address
        :param password: The password for this address
        :param config_template_path: The Ocean() library class *requires* a config file, this is the template
        :param config_path: Or, the address and password are stored in a file already
        """
        self.name = name
        self.address = address
        self.role = role
        self.credentials = False # Does this config file have a user address and pasword?
        if not config_template_path:
            self.config_template_path = PATH_CONFIG
        else:
            self.config_template_path = config_template_path
        self.config_path = config_path

        self.ocn = None # This is the Ocean API instance, per User
        self.account = None

        if config_path:
            # If a config file is directly provided, this User is instantiated directly
            self.ocn = Ocean(config_path)
            logging.info("User instantiated from provided configuration file".format())
        elif password and config_template_path:
            # If the account is unlocked, instantiate Ocean and the Account classes

            # The ocean class REQUIRES a .ini file on instantiation -> need to create this file!
            self.config_fname = "{}_{}_config.ini".format(self.name,self.role).replace(' ', '_')
            this_config_path = self.create_config(password) # Create configuration file for this user

            # Instantiate Ocean and Account for this User
            self.ocn = Ocean(this_config_path)
            if self.ocn.main_account: # If this attribute exists, the password is stored
                self.credentials = True
            logging.info("User instantiated from a newly created configuration file based on template".format())
        else:
            # If nothing is provided, raise an error
            raise ValueError("A User object requires a config.ini file, or a template and password.")


        acct_dict_lower = {k.lower(): v for k, v in self.ocn.accounts.items()}
        if self.ocn.main_account: # If this attribute exists, the password is stored
            self.credentials = True
            self.account = self.ocn.main_account
        else:
            raise ValueError
        logging.info(self)

    def create_config(self, password):
        """Fow now, a new config.ini file must be created and passed into Ocean for instantiation"""
        conf = configparser.ConfigParser()
        # Read in the config template file, and modify it
        conf.read(str(self.config_template_path))
        conf['keeper-contracts']['parity.address'] = self.address
        conf['keeper-contracts']['parity.password'] = password
        out_path = Path.cwd() / 'user_configurations' / self.config_fname
        logging.info("Create a new configuration file for {}.".format(self.name))
        with open(out_path, 'w') as fp:
            conf.write(fp)
        return out_path

    @property
    def locked(self):
        #TODO: This needs to be more robust, just having a password does not mean it's unlocked!
        if self.credentials:
            return False
        else:
            return True

    def __str__(self):
        if not self.credentials:
            return "{:<20} {:<20} LOCKED ACCOUNT".format(self.name, self.role)
        else:
            ocean_token = self.account.ocean_balance
            return "{:<20} {:<20} with {} Ocean token".format(self.name, self.role, ocean_token)

    def __repr__(self):
        return self.__str__()



def get_all_users(addresses):
    users = list()
    if get_deployment_type() == 'DEFAULT':
        for i, acct_address in enumerate(addresses):
            user_name = "User_"+str(i)
            user = User(user_name, "Role", acct_address)
            users.append(user)
    elif get_deployment_type() == 'USE_K8S_CLUSTER' or get_deployment_type() == 'JUPYTER_DEPLOYMENT':
        user_config_path = get_project_path() / 'user_configurations_deployed'
        assert user_config_path.exists()
        for conf_file in user_config_path.glob('*.ini'):
            name = ' '.join(conf_file.name.split('_')[0:2])
            user = User(name, role="Ocean User", address=None, password=None, config_template_path=None, config_path=conf_file)
            users.append(user)
    return users

def get_first_user(addresses):
    """Get the first encountered user in the list of accounts, or first in the .ini files
    TODO: Refactor
    :param addresses:
    :return:
    """
    if get_deployment_type() == 'DEFAULT':
        for i, acct_address in enumerate(addresses):
            user_name = "User_"+str(i)
            user = User(user_name, "Role", acct_address)
            break
    elif get_deployment_type() == 'USE_K8S_CLUSTER' or get_deployment_type() == 'JUPYTER_DEPLOYMENT':
        user_config_path = get_project_path() / 'user_configurations_deployed'
        assert user_config_path.exists()
        for conf_file in user_config_path.glob('*.ini'):
            name = ' '.join(conf_file.name.split('_')[0:2])
            user = User(name, role="Ocean User", address=None, password=None, config_template_path=None, config_path=conf_file)
            break
    return user

def account_unlocked(acct):
    # TODO:
    from squid_py.keeper.web3_provider import Web3Provider
    Web3Provider.get_web3().eth.sign(my_acct.address, text="")

def get_user(role = 'Data Owner'):
    return User