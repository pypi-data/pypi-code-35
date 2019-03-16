import os
import json
import zipfile

class Config(object):

    def __init__(self):
        self.verify_tls = False
        self.__config = {}
        self.__config['auth_token'] = None
        self.__config['url'] = None
        self.__config['username'] = None

        self.__home_dir = os.path.expanduser('~')
        self.__config_dir = os.path.join(self.__home_dir, '.ucp')
        self.__config_path = os.path.join(self.__config_dir, 'config.json')
        self.__bundle_dir = os.path.join(self.__config_dir, 'bundle')
        self.__bundle_path = os.path.join(self.__config_dir, "bundle.zip")
        self.__auth_token_path = os.path.join(self.__config_dir, 'auth_token')
        self.__ensure_configdirs()


    def get_url(self):
        self.__load_config()
        return self.__config["url"]

    def get_authtoken(self):
        self.__load_config()
        return self.__config["auth_token"]

    def set_username(self, username):
        self.__config['username'] = username
        self.__save_config()

    def set_authtoken(self, auth_token):
        self.__config['auth_token'] = auth_token
        self.__save_config()

    def set_url(self, url):
        self.__config['url'] = url
        self.__save_config()

    def __load_config(self):
        with open(self.__config_path, 'r') as fp:
            self.__config = json.load(fp)

    def __save_config(self):
        with open(self.__config_path, 'w') as fp:
            json.dump(self.__config, fp)


    def __ensure_configdirs(self):
        os.makedirs(self.__config_dir, exist_ok=True)
        os.makedirs(self.__bundle_dir, exist_ok=True)


    def __read_auth_token(self, path):
        try:
            with open(path) as f:
                data = json.load(f)
                return data
        except:
            print("Unable to open auth token file...")

    def save_bundle_file(self, data):
        with open(self.__bundle_path, "wb") as write_file:
            write_file.write(data)

    def extract_bundle_file(self):
        try:
            zip = zipfile.ZipFile(self.__bundle_path)
            zip.extractall(self.__bundle_dir)
            zip.close()
        except FileNotFoundError:
            print("Bundle file was not found")
        except zipfile.BadZipfile:
            print("The zipfile was bad...")

    def __file_is_empty(self, path):
        return os.stat(path).st_size==0

if __name__ == "__main__":

    conf = Config()
    auth_token = conf.get_auth_token()
    
    if auth_token == None:
        print("An auth token was not found...")
        print("Please login to get a new one...")
    else:
        printf("Found the auth token: {}".format(auth_token))
        print("Extracting client bundle...")
        conf.extract_bundle_file() 
    
