# coding=utf-8
"""
Created on 2015年11月23日

@author: thomas.ning
"""
import os
import string
import sys
from runner.common.assertion import Assertion

assertion = Assertion()

class ConfigParser(object):
    """
    read test plan, then conversion test collections
    """
    CONFIG_NAME_TEST = 'plan'
    CONFIG_NAME_PROJECT = 'project'

    @staticmethod
    def readTests(path):
        return readTestsFromFile(path)
    
    @staticmethod
    def readProject(path):
        return readProjectFromFile(path)
    @staticmethod
    def writeProject(path, content):
        return writeProjectFile(path, content)

def readTestsFromFile(name):
    if not os.path.exists(name):
        assertion.assertMsg('plan Config file does not exist.')
    abspath = os.path.abspath(name)
    sys.path.append(os.path.dirname(os.path.dirname(abspath)))   
    sys.path.append(os.path.dirname(abspath))  
    tests = []
    with open(name) as f:
        try:
            tests_section = False  # filter real tests
            for line in f.readlines():
                if tests_section:
                    if _isSection(line):
                        break
                    else:
                        o = _getOption(line)
                        if o is not None:
                            try:
                                k = o[0]
                                v = int(o[1])
                                tests.append((k, v))
                            except Exception, e:
                                assertion.assertMsg(e)
#                                 print sys.stderr, str(e)
#                                 sys.exit(2)
                else:
                    if _getSection(line) == 'tests':
                        tests_section = True
        except Exception, e:
#             print sys.stderr, str(e)
            assertion.assertMsg(e)
        finally:
            f.close()
    return tests
 
 
def _isSection(s):
    s = string.strip(s)
    if _isComment(s):
        return False
    return len(s) >= 3 and s[0] == '[' and s[-1:] == ']' and len(string.strip(s[1:-1])) > 0
 
 
def _getSection(s):
    s = string.strip(s)
    if _isSection(s):
        return string.strip(s[1:-1])
    else:
        return None
 
 
def _isOption(s):
    s = string.strip(s)
    if _isComment(s):
        return False
    ls = string.split(s, '=')
    return len(ls) == 2 and len(string.strip(ls[0])) > 0 and len(string.strip(ls[1])) > 0
 
 
def _isComment(s):
    s = string.strip(s)
    return len(s) > 0 and s[0] == '#'
 
 
def _getOption(s):
    if _isOption(s):
        ls = string.split(s, '=')
        return (string.strip(ls[0]), string.strip(ls[1]))
    else:
        return None
   
def readProjectFromFile(name):
    if not os.path.exists(name):
        assertion.assertMsg('proiect Config file does not exist.')
    try:
        project = {}
        for (key,value) in readConfigFile(name,"project"):
            project[key] = value
        try:
            for (key, value) in readConfigFile(name, "monitor"):
                project[key] = value
        except:
            pass
        try:
            for (key, value) in readConfigFile(name, "mode"):
                project[key] = value
        except:
            pass
        return project
    except Exception, e:
        assertion.assertMsg(e)
    except:
        assertion.assertMsg("project config error to stop excute")
    
def readConfigFile(name, section):
    import ConfigParser 
    config = ConfigParser.ConfigParser() 
    config.read(name)
    if section in config.sections():
        return config.items(section)
    else:
        assertion.assertMsg('section not in %s file.'%name)
        
def writeProjectFile(path, content, section="project"):
    import ConfigParser 
    config = ConfigParser.ConfigParser() 
    config.read(path)
    for (key,value) in content.items():
        if key not in ['plan','project','project_addr','test_type']:
            if key in ["adbd_monitor", "power_monitor","adbd_threshold","power_high","power_low"]:
                if "monitor" not in config.sections():
                    config.add_section("monitor")
                config.set("monitor", key, value)
            else:
                config.set("project", key, value)           
    config.write(open(path,'w'))
    
        
        

   
   
