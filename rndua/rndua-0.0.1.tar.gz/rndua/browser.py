import os
import random

class BrowserGenerator:

    def __init__(self):
        self.chrome_versions=[]
        with open(os.path.join(os.path.dirname(__file__),
            'data/chrome.csv')) as chrome_data:
            for line in chrome_data:
                self.chrome_versions.append(line[:-1].split(','))
        self.firefox_versions=[]
        with open(os.path.join(os.path.dirname(__file__),
            'data/firefox.list')) as firefox_data:
            for line in firefox_data:
                self.firefox_versions.append(line[:-1])

    def get_chrome_versions(self):
        return self.chrome_versions

    def get_random_chrome_version(self,minimum=60,maximum=74):
        vers_len=len(self.chrome_versions)
        idx_min=0
        for i in range(vers_len):
            if int(self.chrome_versions[i][0].split('.')[0])==minimum:
                idx_min=i
                break;
        idx_max=vers_len-1
        for i in range(vers_len-1,-1,-1):
            if int(self.chrome_versions[i][0].split('.')[0])==maximum:
                idx_max=i
                break;
        ver=self.chrome_versions[random.randint(idx_min,idx_max)].copy()
        ver[0]+='.'+str(random.randint(0,128))
        return ver

    def get_firefox_versions(self):
        return self.firefox_versions

    def get_random_firefox_version(self,minimum=50,maximum=66):
        vers_len=len(self.firefox_versions)
        idx_min=0
        for i in range(vers_len):
            if int(self.firefox_versions[i].split('.')[0])==minimum:
                idx_min=i
                break;
        idx_max=vers_len-1
        for i in range(vers_len-1,-1,-1):
            if int(self.firefox_versions[i].split('.')[0])==maximum:
                idx_max=i
                break;
        return self.firefox_versions[random.randint(idx_min,idx_max)]
