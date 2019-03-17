#!/usr/bin/python3

"""
 download_cp: an example do_download option usage.

  This launches the 'cp' command with appropriate arguments to perform a file transfer.

  This demonstrates a custom downloading method to work with the message_download on_message 
  plugin.  See that plugin source for more detailed documentation.
  
  This downloader expects to be invoked for the 'download' URL scheme is specified as a URL.

  while the scp command is used by default, it can be overridden with the download_cp_command option.

  Samnple usage:

  download_cp_command /usr/bin/cp -p 

  do_download download_cp

  will instead of instead of invoking cp, it will invoke the cp -p command. To the command will be 
  appended the appropriate source and destination file specifications as per cp command expectations.

"""

import os,stat,time
import calendar

class CP_DOWNLOAD(object): 


   def __init__(self,parent):
      if not hasattr(parent,'download_cp_command'):
         parent.download_cp_command= [ '/usr/bin/cp' ]
      pass
          
   def perform(self,parent):
      logger = parent.logger
      msg    = parent.msg

      import subprocess

      # rebuild an scp compatible source specification from the provide url ( proto://user@host// --> user@host: )

      cmd = parent.download_cp_command[0].split() + [ msg.url.path, msg.new_dir + os.sep + msg.new_file ] 

      logger.debug("download_cp invoking: %s " % cmd )
      
      result =  subprocess.call( cmd )
      
      if (result == 0):  # Success!
         if parent.reportback:
            msg.report_publish(201,'Downloaded')
         if hasattr(parent,'chmod'):
            os.chmod(msg.new_file, parent.chmod)
         return True
         
      #Failure!

      if parent.reportback:
         msg.report_publish(499,'download_cp failed invocation of: %s ' % cmd )

      return False 


cp_download = CP_DOWNLOAD(self)
self.do_download = cp_download.perform

