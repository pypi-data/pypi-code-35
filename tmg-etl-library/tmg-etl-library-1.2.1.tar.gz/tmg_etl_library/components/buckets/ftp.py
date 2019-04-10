from tmg_etl_library.components.buckets.bucket import Bucket

import pysftp
import os


class FTPClient(Bucket):

    def __init__(self, log, hostname, username, password):
        super().__init__(log)
        self.hostname = hostname
        self.username = username
        self.sftp = self._connect(hostname, username, password)

    def _connect(self, hostname, username, password):
        try:
            opts = pysftp.CnOpts()
            opts.hostkeys = None

            cnx = pysftp.Connection(hostname, username=username, password=password, cnopts=opts)
            self.logger.info('Connection established to {}'.format(hostname))
            return cnx
        except pysftp.paramiko.ssh_exception.AuthenticationException:
            self.logger.error('Failed to connect to {}'.format(hostname))
            raise Exception('Authentication Error, check credentials')

    def list_files(self, remote_path=None):
        if remote_path:
            self.sftp.chdir(remote_path)

        found_files = []

        for file in self.sftp.listdir():
            ftpfile = FTPFile(file, remote_path)
            found_files.append(ftpfile)

        if remote_path:
            self.sftp.chdir('/')

        return found_files


class FTPFile:

    def __init__(self, client, file_name, file_path=None):
        self.file_path = file_path
        self.file_name = file_name
        self.full_path = os.path.join(self.file_path, self.file_name)
        if isinstance(client, FTPClient):
            self._client = client
        else:
            raise TypeError('Client should be of FTPClient type')

    @property
    def client(self):
        return self._client

    @client.setter
    def client(self, value):
        raise RuntimeError('The client should not updated after creation of the FTPClient')

    def download(self, file):
        remotepath = self.full_path
        localpath = file.full_path

        self.client.sftp.get(remotepath=remotepath, localpath=localpath)
        self.client.logger.info('Downloaded {}'.format(self.file_name))

        return localpath

    def upload(self, file):
        remotepath = self.full_path
        localpath = file.full_path

        self.client.sftp.put(remotepath=remotepath, localpath=localpath)

        return remotepath

    def delete(self):
        self.client.sftp.remove(self.full_path)
