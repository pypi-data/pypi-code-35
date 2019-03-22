#!/usr/bin/python
# -*- coding:utf-8 -*- 

import os
import json
import datetime
import platform
from tools import TimeoutCommand
from os.path import join, exists

'''error msg if command not found'''
LOCATION_NOT_FOUND_EXCEPTION = '%s not found.'
'''global time stamp format'''
TIME_STAMP_FORMAT = '%Y-%m-%d %H:%M:%S'
'''global test result output file name'''
LOG_FILE_NAME = 'log.txt'
'''global test log output name'''
FAILURE_SNAPSHOT_NAME = 'failure.png'

def _isExecutable(exe):
    '''
    return True if program is executable.
    '''
    return os.path.isfile(exe) and os.access(exe, os.X_OK)

def _findExetuable(program):
    '''
    return the absolute path of executable program if the program available.
    else raise Exception.
    '''
    if platform.system() == "Windows":
        return program
    program_path, program_name = os.path.split(program)
    if program_path:
        if _isExecutable(program):
            return program
    else:
        for path in os.environ['PATH'].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if _isExecutable(exe_file):
                return exe_file
    raise Exception(LOCATION_NOT_FOUND_EXCEPTION % program)

def _wraptime(dt):
    sysstr = platform.system()
    if(sysstr == "Windows"):
        return str(dt).replace(':', '.')
    else:
        return str(dt)

def _time():
    '''
    time stamp format
    '''
    #return time.strftime(TIME_STAMP_FORMAT, time.localtime(time.time()))
    return str(datetime.datetime.now())

def _mkdir(path):
    '''
    create directory as path
    '''
    if not exists(path):
        os.makedirs(path)
    return path

def _writeResultToFile(output, content):
    try:
        with open(output, 'a') as f:
            f.write('%s%s' % (json.dumps(content), os.linesep))
    except:
        pass


class AndroidSystem(object):
    
    @staticmethod
    def writeSSPIDToFile(path):
        try:
            serial = os.environ['ANDROID_SERIAL'] if os.environ.has_key('ANDROID_SERIAL') else None
            bridge = _findExetuable('adb')
            times = '?'
            system_server_pid = '?'
            if serial:
                system_server_pid = TimeoutCommand('%s -s %s shell \"ps | grep system_server\"' % (bridge, serial)).run().strip().split()[1]
                times = TimeoutCommand('%s -s %s shell date' % (bridge, serial)).run().strip()
            else:
                system_server_pid = TimeoutCommand('%s shell \"ps | grep system_server\"' % bridge).run().strip().split()[1]
                times = TimeoutCommand('%s shell date' % bridge).run().strip()
            pid_file = join(path, 'system_server_pid.txt')
            with open(pid_file, 'a') as f:
                f.write('%s -> %s' % (times, system_server_pid))
        except:
            pass
        
    @staticmethod
    def save(path, types='fail'):
        '''
        pull log from device to report folder
        '''
        try:
            serial = os.environ['ANDROID_SERIAL'] if os.environ.has_key('ANDROID_SERIAL') else None
            #snapshot & system log
            bridge = _findExetuable('adb')
            if serial:
                if types == 'fail':
                    TimeoutCommand('%s -s %s shell screencap /sdcard/%s' % (bridge ,serial, FAILURE_SNAPSHOT_NAME)).run()
                    TimeoutCommand('%s -s %s pull /sdcard/%s \"%s\"' % (bridge, serial, FAILURE_SNAPSHOT_NAME, path)).run()
                output = TimeoutCommand('%s -s %s logcat -v time -d' % (bridge, serial)).run()
                with open(join(path, LOG_FILE_NAME), 'w') as o:
                    o.write(output)
                TimeoutCommand('%s -s %s pull /data/log/%s %s' % (bridge, serial, 'logcat.log', path)).run()
                TimeoutCommand('%s -s %s pull /data/log/%s %s' % (bridge, serial, 'logcat.log.1', path)).run()
                TimeoutCommand('%s -s %s pull /data/log/%s %s' % (bridge, serial, 'logcat.log.2', path)).run()
                TimeoutCommand('%s -s %s pull /data/log/%s %s' % (bridge, serial, 'logcat.log.3', path)).run()
            else:
                if types == 'fail':
                    TimeoutCommand('%s shell screencap /sdcard/%s' % (bridge, FAILURE_SNAPSHOT_NAME)).run()
                    TimeoutCommand('%s pull /sdcard/%s \"%s\"' % (bridge, FAILURE_SNAPSHOT_NAME, path)).run()
                output = TimeoutCommand('%s logcat -v time -d ' % bridge).run()
                with open(join(path, LOG_FILE_NAME), 'w') as o:
                    o.write(output)
                TimeoutCommand('%s pull /data/log/%s %s' % (bridge, 'logcat.log', path)).run()
                TimeoutCommand('%s pull /data/log/%s %s' % (bridge, 'logcat.log.1', path)).run()
                TimeoutCommand('%s pull /data/log/%s %s' % (bridge, 'logcat.log.2', path)).run()
                TimeoutCommand('%s pull /data/log/%s %s' % (bridge, 'logcat.log.3', path)).run()       
        except:
            pass
    

class AndroidApp(object):
    
    @staticmethod
    def clearLogcat():
        try:
            serial = os.environ['ANDROID_SERIAL'] if os.environ.has_key('ANDROID_SERIAL') else None
            #clear logcat
            bridge = _findExetuable('adb')
            if serial:
                TimeoutCommand('%s -s %s shell logcat -c' % (bridge, serial)).run()
            else:
                TimeoutCommand('%s logcat -c' % (bridge)).run()
        except:
            pass
    
    @staticmethod
    def save(path, types='fail'):
        try:
            serial = os.environ['ANDROID_SERIAL'] if os.environ.has_key('ANDROID_SERIAL') else None
            #save logcat
            bridge = _findExetuable('adb')
            if serial:
                output = TimeoutCommand('%s -s %s shell logcat -v time -d' % (bridge, serial)).run()
                with open(join(path, LOG_FILE_NAME), 'w') as o:
                    o.write(output)
            else:
                output = TimeoutCommand('%s logcat -v time -d' % (bridge)).run()
                with open(join(path, LOG_FILE_NAME), 'w') as o:
                    o.write(output)
        except:
            pass

class IOSApp(object):
    pass