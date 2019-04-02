import os
import random

class EnvironmentGenerator:

    def __init__(self):
        # from https://apple.fandom.com/wiki/List_of_Mac_OS_versions
        self.os_x_32=['10.4.4','10.4.5','10.4.6','10.4.7','10.4.8',
                '10.4.9','10.4.10','10.4.11','10.5.0','10.5.1',
                '10.5.2','10.5.3','10.5.4','10.5.5','10.5.6','10.5.7',
                '10.5.8','10.6.0','10.6.1','10.6.2','10.6.3','10.6.4',
                '10.6.5','10.6.6','10.6.7','10.6.8','10.7.0','10.7.1',
                '10.7.2','10.7.3','10.7.4','10.7.5']
        self.os_x_64=['10.8.0','10.8.1','10.8.2','10.8.3','10.8.4',
                '10.8.5','10.9.0','10.9.1','10.9.2','10.9.3','10.9.4',
                '10.9.5','10.10.0','10.10.1','10.10.2','10.10.3',
                '10.10.4','10.10.5','10.11.0','10.11.1','10.11.2',
                '10.11.3','10.11.4','10.11.5','10.11.6','10.12.0',
                '10.12.1','10.12.2','10.12.3','10.12.4','10.12.5',
                '10.12.6','10.13.0','10.13.1','10.13.2','10.13.3',
                '10.13.4','10.13.5','10.13.6','10.14.0','10.14.1',
                '10.14.2','10.14.3','10.14.4']

        # from https://en.wikipedia.org/wiki/Windows_NT
        self.windows_nt_32=['3.1','3.5','3.51','4.0','5.0','5.1']
        self.windows_nt_64=['5.2','6.0','6.1','6.2','6.3','10.0']

        self.linux_distro_sig=['Ubuntu; ','Fedora; ','']

        self.android_versions=[]
        with open(os.path.join(os.path.dirname(__file__),
            'data/android.tsv')) as android_data:
            for line in android_data:
                tsv=line[:-1].split('\t')
                output=[tsv[0],tsv[1]]
                dev=[]
                for i in tsv[2].split(','):
                    if i.startswith(' '):
                        dev.append(i[1:])
                    else:
                        dev.append(i)
                output.append(dev)
                self.android_versions.append(output)

    def get_os_x_versions(self,x86=False,x64=True):
        pool=[]
        if x86:
            pool+=self.os_x_32
        if x64:
            pool+=self.os_x_64
        return pool

    def get_random_os_x_version(self,x86=False,x64=True,minimum='10.4.4',
            maximum='10.14.4'):
        pool=self.get_os_x_versions(x86=x86,x64=x64)
        vers_len=len(pool)
        idx_min=0
        for i in range(vers_len):
            if pool[i]==minimum:
                idx_min=i
                break;
        idx_max=vers_len-1
        for i in range(vers_len-1,-1,-1):
            if pool[i]==maximum:
                idx_max=i
                break;
        return pool[random.randint(idx_min,idx_max)]

    def get_windows_nt_versions(self,x86=False):
        pool=[]
        if x86:
            pool+=self.windows_nt_32
        pool+=self.windows_nt_64
        return pool

    def get_random_windows_nt_version(self,x86=False,minimum='6.1',
            maximum='10.0'):
        pool=self.get_windows_nt_versions(x86=x86)
        vers_len=len(pool)
        idx_min=0
        for i in range(vers_len):
            if pool[i]==minimum:
                idx_min=i
                break;
        idx_max=vers_len-1
        for i in range(vers_len-1,-1,-1):
            if pool[i]==maximum:
                idx_max=i
                break;
        return pool[random.randint(idx_min,idx_max)]

    def get_random_linux_distro_firefox_sig(self):
        return self.linux_distro_sig[random.randint(0,
            len(self.linux_distro_sig)-1)]

    def get_android_versions(self):
        return self.android_versions

    def get_random_android_environment(self,minimum='4.0.1',
            maximum='9.0.0'):
        vers_len=len(self.android_versions)
        idx_max=0
        for i in range(vers_len):
            if self.android_versions[i][1]==maximum:
                idx_max=i
                break;
        idx_min=vers_len-1
        for i in range(vers_len-1,-1,-1):
            if self.android_versions[i][1]==minimum:
                idx_min=i
                break;
        res=self.android_versions[random.randint(idx_max,idx_min)].copy()
        return [res[0],res[1],res[2][random.randint(0,len(res[2])-1)]]
