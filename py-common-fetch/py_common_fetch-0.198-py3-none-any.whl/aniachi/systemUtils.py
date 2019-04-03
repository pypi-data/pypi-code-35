from termcolor import colored
import sys
import platform
import datetime
import psutil
import getpass
import os

import collections
import json


import cpuinfo


from aniachi import timeUtils,stringUtils

from json2html import *

from pip._internal.utils.misc import get_installed_distributions



class Welcome:

#
#
#
#
# / ____/ / / / | / / ____/
#  / /_  / / / /  |/ / /     
# / __/ / /_/ / /|  / /___   
#/_/    \____/_/ |_/\____/ 
#

    @staticmethod
    def screen_resolution():
        
        return ('Not implemented yet....')

    

    @staticmethod
    def _get_script():
        l = psutil.Process().cmdline()
        if len(l)==1:
            return l[0]
        else:
            return l[1]
        
#
#
#    
#
# / ____/ / / / | / / ____/
#  / /_  / / / /  |/ / /     
# / __/ / /_/ / /|  / /___   
#/_/    \____/_/ |_/\____/ 
#
    @staticmethod
    def print_welcome(elapsed=timeUtils.elapsedtime(), version='beta',color_d='blue',color_out='magenta',attributes2=['bold']):
        print(colored('+------------------------------------------+',color_out))
        print(colored('Aniachi Technologies.',color_d,attrs=attributes2))
        s = getpass.getuser()+'@'+platform.node()

        
        print(colored('Computer:            ',color_d,attrs=attributes2),colored(s,color_out))
        print(colored('Script:              ',color_d,attrs=attributes2),colored(Welcome._get_script(),color_out))
        print(colored('Api version:         ',color_d,attrs=attributes2),colored(sys.api_version,color_out))
        
        print(colored('Path:                ',color_d,attrs=attributes2),colored(sys.executable,color_out))
        print(colored('Installed Packages:  ',color_d,attrs=attributes2),colored(len(get_installed_distributions()),color_out))


        print(colored('Native Compiler:     ',color_d,attrs=attributes2),colored(platform.python_compiler(),color_out))
        print(colored('Architecture:        ',color_d,attrs=attributes2),colored(platform.processor(),color_out))
        s = platform.machine()+'  '+platform.system()+' Kernel version '+platform.release()
        print(colored('Kernel:              ',color_d,attrs=attributes2),colored(s,color_out))
        
        
        print(colored('CPU Info:            ',color_d,attrs=attributes2),colored(cpuinfo.get_cpu_info()['brand'],color_out))
        print(colored('Screen resolution:   ',color_d,attrs=attributes2),colored(Welcome.screen_resolution(),color_out))

        print(colored('Python Version:      ',color_d,attrs=attributes2),colored(platform.python_version(),color_out))
        print(colored('Processors:          ',color_d,attrs=attributes2),colored(psutil.cpu_count(logical=False),color_out))
        print(colored('Terminal:            ',color_d,attrs=attributes2),colored(Welcome._get_terminal(),color_out))
        print(colored('User:                ',color_d,attrs=attributes2),colored(getpass.getuser(),color_out))
        print(colored('Current process:     ',color_d,attrs=attributes2),colored(psutil.Process().pid,color_out))
        print(colored('Code version:        ',color_d,attrs=attributes2),colored(version,color_out))
        mem = psutil.virtual_memory()
       
        print(colored('Total Memory:        ',color_d,attrs=attributes2),colored(stringUtils.sizeof_fmt(mem.total),color_out))
        
        print(colored('Available Memory:    ',color_d,attrs=attributes2),colored(stringUtils.sizeof_fmt(mem.available),color_out))
        print(colored('Free Memory:         ',color_d,attrs=attributes2),colored(stringUtils.sizeof_fmt(mem.free),color_out))
        print(colored('Used Memory:         ',color_d,attrs=attributes2),colored(stringUtils.sizeof_fmt(mem.used),color_out))
        print(colored('Active Memory:       ',color_d,attrs=attributes2),colored(stringUtils.sizeof_fmt(mem.active),color_out))
        print(colored('Inactive Memory:     ',color_d,attrs=attributes2),colored(stringUtils.sizeof_fmt(mem.inactive),color_out))
        try:
            print(colored('Wired Memory:        ',color_d,attrs=attributes2),colored(stringUtils.sizeof_fmt(mem.wired),color_out))
        except Exception as e:
            print(colored('Wired Memory:        ', color_d, attrs=attributes2),
                  colored('Not available', color_out))
        
        print(colored('Current path:        ',color_d,attrs=attributes2),colored(os.getcwd(),color_out))
        

        print(colored('Current date:        ',color_d,attrs=attributes2),colored(datetime.datetime.now(),color_out))
        print(colored('Elapsed time:        ',color_d,attrs=attributes2),colored(elapsed.getElapsedTime(),color_out))
        print(colored('+------------------------------------------+',color_out))
        
#
#
#
#
# / ____/ / / / | / / ____/
#  / /_  / / / /  |/ / /     
# / __/ / /_/ / /|  / /___   
#/_/    \____/_/ |_/\____/ 
# 
    

    @staticmethod
    def _get_terminal():
        aux = 'Terminal not found'
        try:
            aux = os.ttyname(sys.stdout.fileno()).split(sep='/')[-1]
        except Exception as e:
            pass

        return aux


    @staticmethod
    def get_all_libs(ft='json'):
        installed_packages = get_installed_distributions()
        d = dict()
        for s in  installed_packages:
            d[s.key]=s.version
        od = collections.OrderedDict(sorted(d.items()))

        if (ft == 'json'):
            return json.dumps(od)
        elif (ft == 'html'):
            return json2html.convert(json = json.dumps(od))
            
        

#
#
#    
#
# / ____/ / / / | / / ____/
#  / /_  / / / /  |/ / /     
# / __/ / /_/ / /|  / /___   
#/_/    \____/_/ |_/\____/ 
#
    @staticmethod
    def get_fetchdata(elapsed=timeUtils.elapsedtime(),format='json',  version='beta'):
        d = dict()
        d['Software']='Aniachi Technologies.'
        s = getpass.getuser()+'@'+platform.node()
        d['Computer']=s
        d['Script']=Welcome._get_script()
        d['Api version']=sys.api_version
        d['Path']=sys.executable
        d['Installed Packages']=len(get_installed_distributions())
        d['Native Compiler']=platform.python_compiler()
        d['Architecture']=platform.processor()
        s = platform.machine()+'  '+platform.system()+' Kernel version '+platform.release()
        d['Kernel']=s
        d['CPU Info']=cpuinfo.get_cpu_info()['brand']
        d['Screen resolution']=Welcome.screen_resolution()
        d['Python Version']=platform.python_version()
        d['Processors']=psutil.cpu_count(logical=False)
        d['Terminal']=Welcome._get_terminal()
        d['User']=getpass.getuser()
        d['Current process']=psutil.Process().pid
        mem = psutil.virtual_memory()
        d['Code version']=version
        d['Total Memory']=stringUtils.sizeof_fmt(mem.total)
        d['Available Memory']=stringUtils.sizeof_fmt(mem.available)
        d['Free Memory']=stringUtils.sizeof_fmt(mem.free)
        d['Used Memory']=stringUtils.sizeof_fmt(mem.used)
        d['Active Memory']=stringUtils.sizeof_fmt(mem.active)
        d['Inactive Memory']=stringUtils.sizeof_fmt(mem.inactive)
        try:
            d['Wired Memory']=stringUtils.sizeof_fmt(mem.wired)
        except Exception as e:
             d['Wired Memory']='Not available'

        d['Current path']=os.getcwd()
        d['Current date']=str(datetime.datetime.now())
        d['Elapsed time:']=elapsed.getElapsedTime()

        print(d)

        if format == 'json':
            return json.dumps(d)
        else:
            return d
        


        
    
        




    @staticmethod
    def print_all_libs(color_d='green'):
        installed_packages = get_installed_distributions()
        d = dict()
        maxLen =10
        for s in  installed_packages:
            if len(s.key) > maxLen:
                maxLen = len(s.key)
            d[s.key]=s.version

        maxLen = maxLen+4  
        od = collections.OrderedDict(sorted(d.items()))
        for k, s in od.items():
            print(colored(stringUtils.alingLeft(k,maxLen),color_d),colored(s,'magenta'))
        print(colored('-'*maxLen,'magenta'))
        print(colored('Total libs',color_d),colored(len(od.items()),'magenta'))
        
#
#
#
#
# / ____/ / / / | / / ____/
#  / /_  / / / /  |/ / /     
# / __/ / /_/ / /|  / /___   
#/_/    \____/_/ |_/\____/ 
#
    @staticmethod
    def print_libs_version(libs,color_d='green'):
        #print(color_d)
        d = dict()
        maxLen =10
        installed_packages = get_installed_distributions()
        for s in  installed_packages:
            if (s.key) in libs:
                d[s.key]=s.version
                if len(s.key) > maxLen:
                    maxLen = len(s.key)
        od = collections.OrderedDict(sorted(d.items())) 
        maxLen = maxLen+2
        if len(od) ==0:
            print(colored('-'*maxLen,'magenta'))
            print(colored('Modules not found',color_d))
            print(colored('-'*maxLen,'magenta'))
        else:
            print(colored('-'*maxLen,'magenta'))
            for k, s in od.items():
                print(colored(stringUtils.alingLeft(k,maxLen),color_d),colored(s,'magenta'))
            print(colored('-'*maxLen,'magenta'))
            print(colored('Total modules ',color_d),colored(len(od.items()),'magenta'))
            
            
        
                
#
#
#
#
# / ____/ / / / | / / ____/
#  / /_  / / / /  |/ / /     
# / __/ / /_/ / /|  / /___   
#/_/    \____/_/ |_/\____/ 
#                
        
        



if __name__ == '__main__':

    print(Welcome.get_fetchdata())