import json
import platform
import subprocess
import os
import sys
from google.oauth2 import service_account
from google.cloud import storage


class GCPUtility:
    env = {}  # Use for shell command environment variables
    suppress_output = False
    run_cmd_background = False
    # Windows Specific
    # https://docs.microsoft.com/en-us/windows/desktop/ProcThread/process-creation-flags
    # This is used to run processes in the background on Windows
    CREATE_NO_WINDOW = 0x08000000

    def __init__(self):
        json_str = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON_STR', '')
        if not json_str:
            print("Google credentials cannot be empty! Check the environment variable: {env_var}.".format(env_var='GOOGLE_APPLICATION_CREDENTIALS_JSON_STR'))
            exit(-1)
        service_account_info = json.loads(json_str)
        credentials = service_account.Credentials.from_service_account_info(service_account_info)
        self.storageClient = storage.Client("onepanelio",credentials)
        if platform.system() is 'Windows':
            self.env[str('SYSTEMROOT')] = os.environ['SYSTEMROOT']
            self.env[str('PATH')] = os.environ['PATH']
            self.env[str('PYTHONPATH')] = os.pathsep.join(sys.path)

    def build_full_gcs_url(self, cs_path):
        cs_path = 'gs://{bucket}/{path}'.format(bucket=self.get_dataset_bucket_name(), path=cs_path)
        return cs_path

    def get_dataset_bucket_name(self):
        return os.getenv('DATASET_BUCKET', 'onepanel-datasets')

    def upload_dir(self, dataset_directory, gcs_directory, exclude=''):
        bucket = self.storageClient.get_bucket(self.get_dataset_bucket_name())

        for root, subdirs, files in os.walk(dataset_directory):
            inside_onepanel_dir = False
            file_path_list = root.split(os.path.sep)
            for path_chunk in file_path_list:
                if '.onepanel' == path_chunk:
                    inside_onepanel_dir = True
                    break
            if inside_onepanel_dir:
                continue
            for filename in files:
                root_path_for_gcp = root
                if platform.system() is 'Windows':
                    root_path_for_gcp = root_path_for_gcp.lstrip(".")
                    root_path_for_gcp = root_path_for_gcp.replace("\\","/")
                file_path = os.path.join(root, filename)

                # This will be empty for top-level walking, but not sub-directories
                if not root_path_for_gcp:
                    upload_path = "/".join([gcs_directory, filename])
                else:
                    upload_path = "".join([gcs_directory, root_path_for_gcp])
                    upload_path = "/".join([upload_path, filename])
                blob = bucket.blob(upload_path)
                blob.upload_from_filename(file_path)
                print("Uploaded {file}".format(file=file_path))
        return 0

    def download_all(self, dataset_directory, cs_directory):
        cs_full_path = self.build_full_gcs_url(cs_directory)
        gcp_full_path = self.get_full_path_to_gcp_cli()
        if "gsutil" in gcp_full_path:
            cmd_list = []
            close_fds = False
            if self.run_cmd_background:
                if sys.platform != 'win32':
                    cmd_list.insert(0, 'nice')
                    cmd_list.insert(0, 'nohup')
                    close_fds = True
                else:
                    # /i so that windows doesn't create "%SYSTEM_DRIVE%" folder
                    cmd_list.insert(0, 'start /b /i')
            cmd_list = cmd_list + [gcp_full_path, '-m', 'rsync', '-d','-r', cs_full_path, dataset_directory]
            # Need to pass the command as one long string. Passing in a list does not work when executed.
            cmd = ' '.join(cmd_list)
            if self.run_cmd_background:
                print("Download starting in background.")
            else:
                print("Downloading...")

            # shell=True because we want to intercept the output from the command.
            # And also, it fixes issues with executing the string of commands.
            if self.run_cmd_background:
                if sys.platform != 'win32':
                    subprocess.Popen(args=cmd, env=self.env, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE, shell=True, close_fds=close_fds)
                else:
                    subprocess.Popen(args=cmd, env=self.env, shell=True, close_fds=close_fds,
                                     creationflags=self.CREATE_NO_WINDOW)
            else:
                p = subprocess.Popen(args=cmd, env=self.env, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE, shell=True, close_fds=close_fds)
                suppress_gcs_info = cs_full_path.rsplit('/', 1)[0]
                for line in iter(p.stdout.readline, '' or b''):  # replace '' with b'' for Python 3
                    if self.suppress_output is False:
                        line_str = line.decode()
                        cleaned_line = line_str.replace(suppress_gcs_info, '')
                        sys.stdout.write(cleaned_line)
            return 0
        return -1

    # TODO temporary method - need to redefine interface for above method
    def download_all_background(self, dataset_directory, s3_directory):
        s3_path = 's3://{bucket}/{path}'.format(bucket=self.get_dataset_bucket_name(), path=s3_directory)
        aws_full_path = self.get_full_path_to_aws_cli()

        if 'aws' not in aws_full_path:
            return -1

        cmd_list = []
        close_fds = False
        if sys.platform != 'win32':
            cmd_list.insert(0, 'nice')
            cmd_list.insert(0, 'nohup')
            close_fds = True
        else:
            # /i so that windows doesn't create "%SYSTEM_DRIVE%" folder
            cmd_list.insert(0, 'start /b /i')
        cmd_list = cmd_list + [aws_full_path, 's3', 'sync', s3_path, dataset_directory]
        # Need to pass the command as one long string. Passing in a list does not work when executed.
        cmd = ' '.join(cmd_list)

        # shell=True because we want to intercept the output from the command.
        # And also, it fixes issues with executing the string of commands.
        if sys.platform != 'win32':
            p = subprocess.Popen(args=cmd, env=self.env, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                                 stderr=subprocess.DEVNULL, shell=True, close_fds=close_fds)

            return 0, p
        else:
            p = subprocess.Popen(args=cmd, env=self.env, shell=True, close_fds=close_fds,
                                 creationflags=self.CREATE_NO_WINDOW)

            return 0, p

    def download(self, to_dir, s3_full_path_to_file):
        s3_path = 's3://{bucket}/{path}'.format(bucket=self.get_dataset_bucket_name(), path=s3_full_path_to_file)
        aws_full_path = self.get_full_path_to_aws_cli()
        if "aws" in aws_full_path:
            cmd_list = []
            close_fds = False
            if self.run_cmd_background:
                if sys.platform != 'win32':
                    cmd_list.insert(0, 'nice')
                    cmd_list.insert(0, 'nohup')
                    close_fds = True
                else:
                    # /i so that windows doesn't create "%SYSTEM_DRIVE%" folder
                    cmd_list.insert(0, 'start /b /i')
            cmd_list = cmd_list + [aws_full_path, 's3', 'cp', s3_path, to_dir]
            # Need to pass the command as one long string. Passing in a list does not work when executed.
            cmd = ' '.join(cmd_list)
            if self.run_cmd_background:
                print("Download starting in background.")
                if sys.platform != 'win32':
                    subprocess.Popen(args=cmd, env=self.env, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE, shell=True, close_fds=close_fds)
                else:
                    subprocess.Popen(args=cmd, env=self.env, shell=True, close_fds=close_fds,
                                     creationflags=self.CREATE_NO_WINDOW)
            else:
                print("Downloading...")
                # Also need to execute through the shell
                p = subprocess.Popen(args=cmd, env=self.env, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE, shell=True, close_fds=close_fds)
                suppress_s3_info = s3_path.rsplit('/', 1)[0]
                for line in iter(p.stdout.readline, '' or b''):  # replace '' with b'' for Python 3
                    if self.suppress_output is False:
                        line_str = line.decode()
                        cleaned_line = line_str.replace(suppress_s3_info, '')
                        sys.stdout.write(cleaned_line)
            return 0
        return -1

    def check_s3_path_for_files(self, full_s3_path='', recursive=True):
        ret_val = {'data': None, 'code': -1, 'msg': ''}
        if full_s3_path == '':
            ret_val = {'data': None, 'code': -1, 'msg': 'Need the full s3 path passed in.'}
            return ret_val
        aws_full_path = self.get_full_path_to_aws_cli()
        if "aws" in aws_full_path:
            recursive_arg = ''
            if recursive:
                recursive_arg = '--recursive'
            # Need to pass the command as one long string. Passing in a list does not work when executed.
            cmd = ' '.join([aws_full_path, 's3', 'ls', recursive_arg, '--summarize', full_s3_path])
            # Also need to execute through the shell
            p = subprocess.Popen(args=cmd, env=self.env, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, shell=True)
            p.wait()
            raw_output = p.stdout.readlines()
            for line in raw_output:
                if 'Total Objects' in line.decode():
                    objects_str = line.decode()
                    str_split = objects_str.split(':')
                    # Grab the string of the number
                    string_num = str_split[-1].strip()
                    ret_val = {'data': int(string_num), 'code': 0, 'msg': 'Total files found.'}
                    break
            return ret_val
        return ret_val

    def get_cs_path_details(self, full_cs_path='', total_files=True, total_bytes=True):
        data = {}
        if full_cs_path == '':
            ret_val = {'data': None, 'code': -1, 'msg': 'Need the full google cloud storage path passed in.'}
            return ret_val

        bucket = self.storageClient.get_bucket(self.get_dataset_bucket_name())
        total_files = 0
        total_bytes = 0

        objects_list = bucket.list_blobs(prefix=full_cs_path)
        if objects_list.num_results < 1:
            data['total_bytes'] = total_bytes
            data['total_files'] = total_files
            ret_val = {'data': data, 'code': 0, 'msg': 'Data found.'}
            return ret_val
        else:
            for obj in objects_list:
                total_files += 1
                total_bytes += obj.size

        if total_bytes:
            data['total_bytes'] = total_bytes
        if total_files:
            data['total_files'] = total_files
        ret_val = {'data': data, 'code': 0, 'msg': 'Data found.'}
        return ret_val