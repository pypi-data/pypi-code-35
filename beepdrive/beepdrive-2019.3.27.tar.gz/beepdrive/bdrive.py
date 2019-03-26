import os
import sys
import time
import shutil
import platform
import distutils.dir_util
from getpass import getpass
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions as ec

import beepdrive.utils as utils
from beepdrive.pyside import Error
from beepdrive.utils import is_frozen, frozen_temp_path

if is_frozen:
    base_dir = frozen_temp_path
elif platform.system() == "Linux":
    base_dir = os.path.join(os.path.expanduser("~"), ".local")
else:
    base_dir = sys.prefix

class BeepDrive:
    def __init__(self, temp_path, folder_path=None):
        # Download variables
        self.courses = dict()
        self.downloaded = -1
        self.beep_url = r"https://beep.metid.polimi.it/polimi/login"

        # Set temp and folder path
        self.temp_path = temp_path
        self.folderpath = folder_path

        self.driver = None

    def set_options(self):
        # Set chrome options
        options = Options()
        options.headless = True
        options.add_argument("log-level=3")
        options.add_argument("window-size=1200x600")
        options.add_experimental_option("prefs", {
            "download.default_directory": self.temp_path,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": False,
            "safebrowsing.disable_download_protection": True
        })

        return options

    def create_driver(self):
        system = platform.system()

        # Get chromedriver path
        if system == "Darwin":
            chromedriver = os.path.join(base_dir, "lib/chromedriver_mac64")
        elif system == "Windows":
            chromedriver = os.path.join(base_dir, "lib/chromedriver_win32.exe")
        elif system == "Linux":
            chromedriver = os.path.join(base_dir, "lib/chromedriver_linux64")

        # Create chromedriver headless instance
        try:
            self.driver = webdriver.Chrome(executable_path=chromedriver, options=self.set_options())
        except WebDriverException:
            # Open dependencies error
            _ = Error()

            sys.exit(0)

        self.enable_headless_download(self.driver)

        # Connect to https://beep.metid.polimi.it/
        sys.stdout.write(r"Connecting to https://beep.metid.polimi.it/ ")
        sys.stdout.flush()
        self.driver.get(self.beep_url)

    def aunica_login(self, queue, person_code, password):
        # Login to https://aunicalogin.polimi.it/
        self.driver.find_element(By.ID, "login").send_keys(person_code)
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.NAME, "evn_conferma").click()

        print("")

        result = self.check_login()

        if queue:
            queue.put(result)

        return result

    def check_login(self):
        html = self.driver.execute_script("return document.body.outerHTML;")

        if "Code: 7" in html:
            # Wrong password
            print("Wrong password.")

            return 7

        if ("Code: 1" in html or
                "Code: 14" in html or
                "Code: 129" in html):
            # Wrong person code
            print("Person code not valid.")

            return 14

        if "Code: 24" in html:
            # Empty password
            print("Empty password.")

            return 24

        if ("La password scadrà" in html or
                "The password will expire" in html):
            # Continue to next page
            self.driver.find_element(By.NAME, "evn_continua").click()

        return 0

    def get_courses(self):
        # Connect to beep
        login = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located((By.ID, "login")))
        login.click()

        # Parse html
        html = self.driver.execute_script("return document.body.outerHTML;")
        soup = BeautifulSoup(html, "html.parser")

        # Get courses table
        table = soup.find("table", {"class": "taglib-search-iterator footable"})
        tbody = table.find("tbody")

        for tr in tbody.findAll("tr"):
            td = tr.find("td")
            a = td.find("a")

            course_name = a.get_text()
            course_url = a["href"]

            # Remove unwanted, format name and update dict
            if (course_name != "BeeP channel" and
                    course_name != "Mobilità internazionale"):
                if '-' in course_name:
                    course_name = course_name.split(" - ")[1].lower().title()
                else:
                    course_name = course_name.lower().title()

                course_name = course_name.replace("[ ", '(').replace(" ]", ')')

                self.courses[course_name] = course_url

    def start_download(self, folderpath=None, selected=None):
        # Get folder path if GUI enabled
        if folderpath:
            self.folderpath = folderpath

        # Folder path format
        if self.folderpath[-1:] != '/':
            self.folderpath = self.folderpath + '/'

        # No change if GUI disabled
        if not selected:
            selected = self.courses

        # Elaborate each course page
        for key, value in self.courses.items():

            if selected[key]:
                # Increase downloaded number
                self.downloaded += 1

                # Get documents and media page
                self.driver.get(value)
                url = self.driver.current_url
                url = url.replace("attivita-online-e-avvisi", "documenti-e-media")
                self.driver.get(url)

                # Loop on every download
                j, loop = 2, True
                while loop:
                    widget_buttons = self.driver.find_elements(By.CLASS_NAME, "nobr")

                    # The first two buttons are not relevant
                    if len(widget_buttons) < 3:
                        loop = False
                    else:
                        i = 0

                        for i in range(j, len(widget_buttons)):
                            # Open and focus widget
                            widget_buttons[i].click()
                            widget = self.driver.find_element(By.CLASS_NAME, "aui-overlay-focused")

                            # Move cursor up if single file
                            if '(' in widget.text:
                                widget.find_element(By.CLASS_NAME, "last").click()
                            # Move cursor down if folder
                            else:
                                widget.find_element(By.CLASS_NAME, "taglib-icon").click()

                            # Read page_error() comments
                            if self.page_error():
                                self.driver.back()
                                j = i + 1
                                break

                        # If all possible downloads launched
                        if i == len(widget_buttons) - 1:
                            loop = False

                # Wait all course specific downloads to complete
                self.wait_for_download()

                # Move files to desired folder
                self.move_files(key)

                # Reset folder
                if os.path.exists(self.temp_path):
                    shutil.rmtree(self.temp_path)

                os.makedirs(self.temp_path)

    def page_error(self):
        errors = []
        html = self.driver.execute_script("return document.body.outerHTML;")

        # Italian errors
        errors.append("temporaneamente non disponibile")
        errors.append("dimensioni troppo grandi per essere scaricata")

        # English errors
        errors.append("temporarily unavailable")
        errors.append("size of the folder is very high to be downloaded")

        return any(error in html for error in errors)

    def wait_for_download(self):
        downloading = True

        # While still downloading
        while downloading:
            source = os.listdir(self.temp_path)

            # If folder empty
            if not source:
                downloading = False
            else:
                i = 0

                for i, value in enumerate(source):
                    if value.endswith(".crdownload"):
                        i -= 1
                        break

                # All files completed
                if i == len(source) - 1:
                    downloading = False

    def move_files(self, course):
        time.sleep(1)

        # Create course folder
        if not os.path.exists(self.folderpath + course):
            os.makedirs(self.folderpath + course)

        # Unzip files in course folder
        utils.unzip_directory_recursively(self.temp_path)

        # Move files to specified folder
        distutils.dir_util.copy_tree(
            self.temp_path,
            self.folderpath + course + '/',
            update=1,
        )

    def enable_headless_download(self, driver):
        # Enable chrome headless download feature
        driver.command_executor._commands["send_command"] = ("POST", r"/session/$sessionId/chromium/send_command")
        params = {"cmd": "Page.setDownloadBehavior", "params": {"behavior": "allow", "downloadPath": self.temp_path}}
        _ = driver.execute("send_command", params)

    def quit(self):
        # Quit chromedriver
        self.driver.quit()

    def run(self):
        try:
            self.create_driver()

            logged = False

            while not logged:
                person_code = input("\nPerson code: ")
                password = getpass("Password: ")

                if not self.aunica_login(None, person_code, password):
                    logged = True

            self.get_courses()
            self.start_download()
        except KeyboardInterrupt:
            pass

        self.quit()

# Override selenium service.py
# try:
#             cmd = [self.path]
#             cmd.extend(self.command_line_args())
#             self.process = subprocess.Popen(cmd, env=self.env,
#                                             close_fds=platform.system() != 'Windows',
#                                             stdout=PIPE,
#                                             stderr=PIPE,
#                                             stdin=PIPE,
#                                             creationflags=0x08000000)
#         except TypeError:
#             raise
