from selenium.webdriver import ChromeOptions
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import FirefoxProfile

class WebChromeOptions(ChromeOptions):

    def background(self):
        self.add_argument('--headless')
    
    def private(self):
        self.add_argument('--incognito')
    
    def maximized(self):
        self.add_argument('--start-maximized') 

    def set_path_user(self,perfil_path):
        self.options.add_argument('user-data-dir={}'.format(perfil_path))

    def window_size(self,width,heigth):
        self.add_argument('--window-size={},{}'.format(width,heigth))

    def window_position(self,x,y):
        self.add_argument('--window-position={},{}'.format(x,y))

    def set_proxy(self,proxy):
        self.add_argument('--proxy-server={}'.format(proxy))


def WebFirefoxOptions(Options):

    def background(self):
        self.headless=True


def WebFirefoxProfile(FirefoxProfile):

    def private(self):
        self.set_preference("browser.privatebrowsing.autostart", True)