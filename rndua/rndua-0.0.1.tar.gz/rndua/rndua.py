from rndua.browser import BrowserGenerator
from rndua.environment import EnvironmentGenerator
from rndua.format import Formatter

import random

class RandomUAGenerator():
    def __init__(self):
        self.bg=BrowserGenerator()
        self.eg=EnvironmentGenerator()
        self.fm=Formatter()

    def get_random_android_chrome_ua(self,chrome_minimum=60,
            chrome_maximum=74,android_minimum='4.0.1',
            android_maximum='9.0.0'):
        return self.fm.format_chrome_ua(
                self.fm.android_environment_to_ua(
                    self.eg.get_random_android_environment(
                        minimum=android_minimum,maximum=android_maximum)),
                self.bg.get_random_chrome_version(minimum=chrome_minimum,
                    maximum=chrome_maximum))

    def get_random_android_firefox_ua(self,firefox_minimum=50,
            firefox_maximum=66,android_minimum='4.0.1',
            android_maximum='9.0.0'):
        return self.fm.format_firefox_ua(
                self.fm.android_environment_to_ua(
                    self.eg.get_random_android_environment(
                        minimum=android_minimum,maximum=android_maximum),
                    firefox=True),self.bg.get_random_firefox_version(
                        minimum=firefox_minimum,maximum=firefox_maximum),
                    desktop=False)

    def get_random_windows_chrome_ua(self,chrome_minimum=60,
            chrome_maximum=74,windows_minimum='6.1',windows_maximum='10.0'):
        return self.fm.format_chrome_ua(
                self.fm.windows_nt_version_to_ua(
                    self.eg.get_random_windows_nt_version(
                        minimum=windows_minimum,maximum=windows_maximum),),
                self.bg.get_random_chrome_version(minimum=chrome_minimum,
                    maximum=chrome_maximum))

    def get_random_windows_firefox_ua(self,firefox_minimum=50,
            firefox_maximum=66,windows_minimum='6.1',windows_maximum='10.0'):
        return self.fm.format_firefox_ua(
                self.fm.windows_nt_version_to_ua(
                    self.eg.get_random_windows_nt_version(
                        minimum=windows_minimum,maximum=windows_maximum),),
                    self.bg.get_random_firefox_version(
                        minimum=firefox_minimum,maximum=firefox_maximum),)
    
    def get_random_os_x_chrome_ua(self,chrome_minimum=60,
            chrome_maximum=74,os_x_minimum='10.4.4',os_x_maximum='10.14.4'):
        return self.fm.format_chrome_ua(
                self.fm.os_x_version_to_chrome(
                    self.eg.get_random_os_x_version(
                        minimum=os_x_minimum,maximum=os_x_maximum),),
                self.bg.get_random_chrome_version(minimum=chrome_minimum,
                    maximum=chrome_maximum))

    def get_random_os_x_firefox_ua(self,firefox_minimum=50,
            firefox_maximum=66,os_x_minimum='10.4.4',os_x_maximum='10.14.4'):
        return self.fm.format_firefox_ua(
                self.fm.os_x_version_to_firefox(
                    self.eg.get_random_os_x_version(
                        minimum=os_x_minimum,maximum=os_x_maximum),),
                    self.bg.get_random_firefox_version(
                        minimum=firefox_minimum,maximum=firefox_maximum))

    def get_random_linux_chrome_ua(self,chrome_minimum=60,
            chrome_maximum=74):
        return self.fm.format_chrome_ua('X11; Linux x86_64',
                self.bg.get_random_chrome_version(minimum=chrome_minimum,
                    maximum=chrome_maximum))

    def get_random_linux_firefox_ua(self,firefox_minimum=50,
            firefox_maximum=66,os_x_minimum='10.4.4',os_x_maximum='10.14.4'):
        return self.fm.format_firefox_ua(''.join(['X11; ',
            self.eg.get_random_linux_distro_firefox_sig(),'Linux x86_64']),
            self.bg.get_random_firefox_version(
                minimum=firefox_minimum,maximum=firefox_maximum))

    def get_random_ua(self):
        val=random.randint(0,100)
        if val>=95:
            return self.get_random_os_x_chrome_ua()
        if val>=90:
            return self.get_random_os_x_firefox_ua()
        if val>=85:
            return self.get_random_os_x_chrome_ua()
        if val>=70:
            return self.get_random_os_x_firefox_ua()
        if val>=50:
            return self.get_random_windows_chrome_ua()
        if val>=40:
            return self.get_random_windows_firefox_ua()
        if val>=5:
            return self.get_random_android_chrome_ua()
        return self.get_random_android_firefox_ua()
