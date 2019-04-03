"""Memory Profyler"""
import datetime
import time
import math
import os
import re
import sys
import psutil
import inspect
import numpy as np

class ProfylerException(Exception):
    """
    Exception Class
    """
    __module__ = Exception.__module__
    def __init__(self, error):
        try:
            line = sys.exc_info()[-1].tb_lineno
        except AttributeError:
            line = inspect.currentframe().f_back.f_lineno
        self.args = f"{type(self).__name__} (line {line}): {error}",
        sys.exit(self)

class Colors:
    PURPLE    = '\033[95m'
    BLUE      = '\033[94m'
    GREEN     = '\033[92m'
    YELLOW    = '\033[93m'
    RED       = '\033[91m'
    WHITE     = '\033[0m'
    UNDERLINE = '\033[4m'

class PyProfyler(object):
    """
    Memory Profyler Class
    """
    def __get_elapsed_time(self, start):
        """
        An assistant helper function:
            calculates elapsed time.
        """
        return datetime.timedelta(time.time() - start)
    def __get_process_memory(self):
        """
        An assistant helper function:
            assists in getting memory info.
        """
        meminfo = psutil.Process(os.getpid()).memory_info()
        return np.array([meminfo.rss, meminfo.vms, meminfo.shared])
    def __format_bytes(self, bytes):
        """
        An assistant helper function:
            assists in converting sizes to B, KB, MB, GB values.
        """
        memsize = (1, abs(bytes)) [abs(bytes)>0]
        units   = {3:"B", 6:"KB", 9:"MB", 12:"GB"}
        unit    = min(i for i in units.keys() if i > math.floor(np.log10(memsize)))
        return str(round(bytes/10** math.floor(np.log10(memsize)), 2)) + units[unit]
    def __oneliner(self, x):
        """
        An assistant helper function:
            assists in pretty printing,
            by removing white spaces after newlines.
        """
        return re.sub(r"\n\s*" , " " , x)
    def __init__(self, func, *args, **kwargs):
        """
        A main function:
            performs main functionality: wrapping execution -> formatting.
        """
        self.profiled   = False
        self.func = func
        self.args      = args
        self.kwargs    = kwargs
        def wrapper(self, *args, **kwargs):
            stats      = self.__get_process_memory()
            starttime  = time.time()
            result     = self.func(*args, **kwargs)
            timeperiod = self.__get_elapsed_time(starttime)
            stats      = self.__get_process_memory() - stats
            self.profile = self.__oneliner(
                                          f"""{Colors.GREEN}
                                              Profile: {self.func.__name__:>20} |
                                              RSS:  {self.__format_bytes(stats[0]):>08} | 
                                              VMS:  {self.__format_bytes(stats[1]):>08} | 
                                              SHR:  {self.__format_bytes(stats[2]):>08} | 
                                              UpTime: {timeperiod} 
                                              {Colors.WHITE}"""
                                          )
            return result
        self.wrapper = wrapper
    def __call__(self):
        """
        A main function:
            makes the class callable.
            responsible for delayed execution.
        """
        self.profiled = True
        return self.wrapper(self, *self.args, **self.kwargs)
    def __str__(self):
        """
        A main function:
            makes the class printable.
        """
        if not self.profiled:
            return self.__oneliner(f"""{Colors.YELLOW} 
                                      {self.func.__name__} 
                                      hasn't been executed yet. 
                                      {Colors.WHITE}""")
        else:
            return self.profile
    def __getitem__(self, key):
        """
        A main function:
            makes the class subscriptable.
        """
        if key != "profile":
            raise ProfylerException(f"{Colors.RED} Key Error. {Colors.WHITE}")
        return self.__str__()