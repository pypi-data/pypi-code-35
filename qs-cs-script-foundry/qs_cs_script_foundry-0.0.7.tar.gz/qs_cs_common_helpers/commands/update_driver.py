import zipfile
import cloudshell.api.cloudshell_api as cs_api
import os

class driver_updater():
    def __init__(self, credentials, custom_driver_name=None):
        self.default_directory_name = os.path.basename(os.getcwd())
        self.driver_name = custom_driver_name or self.default_directory_name
        self.zip_address = self.driver_name + '.zip'
        self.establish_cs_session(credentials=credentials)

    def zip_files(self):
        z = zipfile.ZipFile(self.zip_address, "w")
        files_to_exclude = [self.zip_address, "venv", ".idea"]
        all_files = []

        for path, subdirs, files in os.walk('.'):
            for f in files:
                if f not in files_to_exclude and not f.endswith('.pyc'):
                    all_files.append(os.path.join(path, f))

        for script_file in all_files:
            z.write(script_file)

        z.close()

        if self.zip_address in os.listdir('.'):
            print("[+] ZIPPED UP: '{zip_address}'".format(zip_address=self.zip_address))
        else:
            print("[-] ZIP FILE DOES NOT EXIST")


    def establish_cs_session(self, credentials):
        try:
            self.cloudshell_session = cs_api.CloudShellAPISession(host=credentials["server"],
                                              username=credentials["user"],
                                              password=credentials["password"],
                                              domain=credentials["domain"])
        except Exception as e:
            print("[-] THERE WAS AN ERROR ESTABLISHING CLOUDSHELL API SESSION" + "\n" + str(e))
            exit(1)



    def update_driver(self):
        try:
            self.cloudshell_session.UpdateDriver(self.driver_name, self.zip_address)
        except Exception as e:
            print("[-] THERE WAS AN ERROR UPDATING SCRIPT\n" + str(e) + "\nPLEASE LOAD SCRIPT MANUALLY THE FIRST TIME")
            exit(1)
        else:
            print("[+] SUCCESFULLY UPDATED IN PORTAL: '{script}'".format(script=self.driver_name))


    def load_to_cs(self):
        self.zip_files()
        self.update_driver()






