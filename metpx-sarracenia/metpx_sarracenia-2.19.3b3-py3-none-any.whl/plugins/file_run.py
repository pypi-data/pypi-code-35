#!/usr/bin/python3

"""
 file_run: 

  Run a command on receipt of each file.

  NOTE: if you are receiving multiple products per second, launching a process for each one
  is probably a bad idea.  You only want to use this if the rate of launching is less than that.

  file_run_command /usr/bin/touch

  do_download file_run

  defaults to running echo.

  current working directory is the one in which the file is to be written.


"""

import os,stat,time
import calendar

class FILE_RUN(object): 


   def __init__(self,parent):
      if not hasattr(parent,'file_run_command'):
         parent.file_run_command= [ '/usr/bin/echo' ]
      pass
          
   def perform(self,parent):
      logger = parent.logger
      msg    = parent.msg

      import subprocess

      # rebuild an scp compatible source specification from the provide url ( proto://user@host// --> user@host: )
      sourcefile = msg.url.hostname + ':' + msg.url.path

      if msg.url.username:
           sourcefile = msg.url.username +'@' + sourcefile

      cmd = parent.file_run_command[0].split() + [ sourcefile, msg.new_file ] 

      logger.debug("file_run invoking: %s " % cmd )
      
      result =  subprocess.call( cmd )
      
      if (result == 0):  # Success!
         if parent.reportback:
            msg.report_publish(201,'Downloaded')
         return True
         
      #Failure!

      if parent.reportback:
         msg.report_publish(499,'file_run failed invocation of: %s ' % cmd )

      return False 


file_run = FILE_RUN(self)
self.on_file = file_run.perform

