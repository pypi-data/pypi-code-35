#!/usr/bin/env python3

#══════════════════════════════════════════════════════════════════════════════════════════════════════════════════
# Class:   SSH_Operation
#──────────────────────────
# Author:  Hengyue Li
#──────────────────────────
# Version: 
#          2019/03/16
#                new upload function, to upload dir without compression.   
#          2019/03/09: 
#                1. rebuilt interface of InteractiveConnectionSSH
#                2. change filename to from RemoteContral1
#                3. make a package contains interface.py
#          2019/03/01
#          2018/06/01
#          2018/02/28
#          2017/09/04
#──────────────────────────
# discription:
#          operation between local PC with a remote server
#          remember to call connect or disconnect for some function.
#
#──────────────────────────
# Imported :
#     shutil , tempfile , stat
import paramiko
import shutil,os,tempfile,random
from .interactive import *  
# import SSH_Operation.interactive as interactive
#──────────────────────────
# Interface:
#
#        [ini] SSHDict   ( see details in paramiko )
#
#        [sub] connect()
#              connect to server.
# 
#        [sub] connectIfNotConnected()  
#
#        [sub] disconnect()
#              disconnect to server.
#
#        [fun] IsRemotePathExist(remotepah)
#              check if a remote path is existed or not.
#
#        [fun] IsRemoteDirExisted(remotepah):
#              for a given remote path, check if it is directory and existed.
#
#        [fun] RemoveRemoteDIr(remoeDir):
#              remove remote directory
#
#        [fun] send_commandlist(commandlist)
#              return error
#
#        [sub] upload_file(localfile,remotedestination)
#              if we call self.upload_file( "test.file"   ,   "/here"  )
#              then "test.file" will be renamed to "here" and be put at root ("/").
#              if there is file (the same name as localfile) existed at server, it will be coverd.
#
#        [sub] download_file(remotefile,localdestination)
#              the "remotefile" will be copied and be saved as "localdestination"
#              "remotefile" and "localdestination"  are all files exactly. The same as upload
#
#        [sub] CompressUploadDir(localdirectoy,remotedestination): !!!! linux dependent ("tar" is used)
#              The upload file can only be directory and compression will be used. Faster!
#              usage:
#                    localdirectoy     = "some/path/directory"
#                    remotedestination = "other/path"
#              the directory would be put at:    "other/path/directory"
#
#        [sub] upload_dir(localdirectoy,remotedestination)
#              the same as CompressUploadDir without compression
#
#        [sub] CompressDownloadDir(Remotedirectoy,localdestination): !!!! linux dependent ("zip/unzip" is also used)
#              The download file can only be directory and compression will be used. Faster!
#              usage:
#                    Remotedirectoy   = "some/path/directory"
#                    localdestination = "other/path"
#              the directory would be put at:    "other/path/directory"
#              This function is not well designed. Tempral file will be created in the folder.
#              But it looks working fine.
#
#-------------------------------------------------------------------------------------
#             ||     linux server actions    ||
#-------------------------------------------------------------------------------------
#        [fun] IsUserExist(username):
#              return True of False
#              check if username is exist in remote server.
#
#        [fun] CreatUser(username):
#              return possible errors.
#              1. Maybe only root user can use this command.
#              2. not forget to call IsUserExist to check if it is existed or not!
#
#        [fun] RemoveUser(username):
#              like "CreatUser".
#
#        [fun] GetHomePath():     (make connection before this sub)
#              get the home path of the remote
#
#══════════════════════════════════════════════════════════════════════════════════════════════════════════════════














class SSH_Operation(object):
    def __init__(self,  SSHDict):
        self.connected =  False
        self.SSHDict   =  dict(SSHDict)



    # return a new SSH connection    # use SSH.close() to disconnected from SSH
    def __get_new_ssh(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(**self.SSHDict)
        return ssh
    # have the input connection SSH disconnected.
    def __disconnect_ssh(self,SSH):
        SSH.close()

    def __check_connected_stop(self):
        if not self.connected:
            print("ssh is not connected while one is trying to use it")
            exit()


    def connect(self):
        self.connected = True
        self.ssh  = self.__get_new_ssh()
        self.sftp = self.ssh.open_sftp()
        
    def connectIfNotConnected(self):
        if not self.connected: self.connect()

    def disconnect(self):
        self.connected = False
        self.sftp.close()
        self.ssh.close()



    def send_commandlist(self,commandlist):
        com=""
        for jc in commandlist:
            com=com+jc+";"
            stdin, stdout, stderr = self.ssh.exec_command(com)
            r=stdout.readlines()
            re=stderr.readlines()
            r=r+re
        return r

    @staticmethod
    def GetProgressbar():
        def viewBar(a,b):
            import sys
            res  = a/int(b)*100
            tsiz = b/1000/1000
            sys.stdout.write("\rComplete precent: {:3.2f}% of total: {:3.2f}M".format(res,tsiz) )
            sys.stdout.flush()
        return viewBar




    def upload_file(self,localfile,remotedestination):
        progressbar = self.GetProgressbar()
        #-------------------------------------------------------------
        self.sftp.put(localfile, remotedestination,callback = progressbar)
        print('')

    def download_file(self,remotefile,localdestination):
        self.sftp.get(remotefile, localdestination)  
        
        
    def upload_dir(self,localdirectoy,remotedestination):
        #------------------------------------------------
        # https://stackoverflow.com/questions/4409502/directory-transfers-on-paramiko
        class MySFTPClient(paramiko.SFTPClient):
            def put_dir(self, source, target):
                ''' Uploads the contents of the source directory to the target path. The
                    target directory needs to exists. All subdirectories in source are 
                    created under target.
                '''
                for item in os.listdir(source):
                    itempath = os.path.join(source, item)
                    if os.path.isfile(itempath):
                        print("send: {}".format(itempath))
                        self.put(itempath, '%s/%s' % (target, item))
                    else:
                        self.mkdir('%s/%s' % (target, item), ignore_existing=True)
                        self.put_dir(itempath, '%s/%s' % (target, item))

            def mkdir(self, path, mode=511, ignore_existing=False):
                ''' Augments mkdir by adding an option to not fail if the folder exists  '''
                try:
                    super(MySFTPClient, self).mkdir(path, mode)
                except IOError:
                    if ignore_existing:
                        pass
                    else:
                        raise
        #-------------------------------------------------------
        fname = os.path.basename(localdirectoy)
        folderpath = remotedestination+"/"+fname
        self.send_commandlist([  "rm -r -f "+folderpath   ])
        self.sftp.mkdir(folderpath) 
        transport = self.ssh.get_transport()
        sftp = MySFTPClient.from_transport(transport)
        sftp.mkdir(remotedestination, ignore_existing=True)
        sftp.put_dir(localdirectoy,folderpath)
        sftp.close()




    # from : https://stackoverflow.com/questions/850749/check-whether-a-path-exists-on-a-remote-host-using-paramiko
    def __pathexisted__(self,sftp, path):
        """os.path.exists for paramiko's SCP object
        """
        # r = True
        try:
            sftp.stat(path)
        except IOError as e:
            r =  False
        else:
            r = True
        return r

    def IsRemoteDirExisted(self,path):
        from stat import S_ISDIR
        try:
            return S_ISDIR(self.sftp.stat(path).st_mode)
        except IOError:
            return False


    def IsRemotePathExist(self,path):
        return self.__pathexisted__(self.sftp, path)

    def RemoveRemoteDIr(self,path):
        import os
        files = self.sftp.listdir(path=path)
        for f in files:
            filepath = os.path.join(path, f)
            if self.IsRemoteDirExisted(filepath):
                self.RemoveRemoteDIr(filepath)
            else:
                self.sftp.remove(filepath)
        self.sftp.rmdir(path)


    def IsUserExist(self,usernamestr):
        self.connect()
        feedback = self.send_commandlist(["grep "+usernamestr+" /etc/passwd"])
        if len(feedback)==0:
            r = False
        else:
            r = True
        return r

    def CreatUser(self,username):
        return self.send_commandlist([  "useradd " + username  ])

    def RemoveUser(self,username):
        return self.send_commandlist([  "userdel -r " + username  ])


    def CompressUploadDir(self,localdirectoy,remotedestination):
        # print(localdirectoy,remotedestination,999)
        #---------set a temp save local zip-------------------
        tmpdir     = tempfile.mkdtemp()  # a temp directory
        tempename  = "Tf"+str(random.randint(999999999, 999999999999)) # temp zip name without suffix
        compresedf = tempename+".tar"
        tmpcfpath  = os.path.join(tmpdir, tempename)
        #--------get directory Name---------------------------
        fname = os.path.basename(localdirectoy)
        #-------get a temperfile name: tempename--------------
        shutil.make_archive(tmpcfpath, "tar", localdirectoy)
        
        #-------check if file existed and remove------------------------------
        folderpath = remotedestination+"/"+fname
        self.send_commandlist([  "rm -r -f "+folderpath   ])
        # print('here',folderpath)
        #-------make a folder-------------------------------------------------
        self.sftp.mkdir(folderpath)                                                #;print(tmpcfpath+".tar")
        
        #-------upload temp file------------------------------
        self.upload_file(tmpcfpath+".tar",folderpath+"/"+compresedf)               #;print("ok1")
        #-------remove local temp file
        shutil.rmtree(tmpdir)
        #------unzip file -----------------------
        self.send_commandlist([  "cd "+folderpath+";"+"tar -xf "+ compresedf +"> /dev/null"  ])   #;print("ok2")
        #------remove remote zip-----------------
        self.send_commandlist([  "cd "+folderpath+";"+"rm -r -f "+compresedf ])                   #;print("ok3")
        #------

    def CompressDownloadDir(self,Remotedirectoy,localdestination):
        import os
        foldername   = os.path.basename(Remotedirectoy)
        dirpath      = os.path.dirname(Remotedirectoy)
        tempzip      = 'tempzip20180416.tar'
        tempzippath  = os.path.join(dirpath,tempzip)
        self.send_commandlist([
        'cd {}'.format(dirpath)                ,
        'tar -czvf  {} {}'.format(tempzip,foldername) ,
        ])
        localzip = os.path.join(localdestination,tempzip)
        self.download_file(tempzippath,localzip)
        self.send_commandlist(['rm {}'.format(tempzippath)])
        shutil.unpack_archive(tempzip,localdestination,'tar' )
        os.remove(tempzip)
        #os.system('cd {};unzip -xo {} > /dev/null; rm {}'.format(localdestination,tempzip,tempzip))


    def GetHomePath(self):
        stdin, stdout, stderr = self.ssh.exec_command("pwd")
        return stdout.readlines()[0].split('\n')[0]
        
     
    def CreateInteractiveConnectionSSH(self):
        #interactive is imported from interactive.py
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(**self.SSHDict)
        channel = client.get_transport().open_session()
        channel.get_pty()
        channel.invoke_shell()
        interactive_shell(channel)
        
    
    
        
