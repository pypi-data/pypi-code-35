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
        json_str = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON_STR', '{"type": "service_account","project_id": "onepanelio","private_key_id": "2eff59c1256e14e88dda2eb97dd9bc0c8f11db96","private_key": "-----BEGIN PRIVATE KEY-----\\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCfTwpzXYDAnwlM\\nPiNWAk+WwPfufWtIMRfrt1QuJHnukUXwBk0mtLQHleTcI7ny4rO8Dbv5RIbbWOBD\\nv1fj16BgAtUMiDTocgMBHrngWyBUv6DO5IVEdgZGlZFiO672g7cPV9/A2JqFgg1g\\nXA5fA5CKB/JIjNo9ENwqEwp553zGBRKBXCL2FQB7Yy7SzmUipze1oE++KCWSWNUC\\nGF508cB2TT8hRvCs6UCldBsZD152dBmoeEVU2P5C1dgcZfDgqm5YXcbCaq+N/ICW\\n2PMe3073aY3WY8jPf1sN55epA6a57DDfDN2Fv7PcT8HjU5SpcQmNt/CBTjD8/XY9\\nsQciQjQBAgMBAAECggEABigN0ADbCuvvy2HTXRg1xIOskSuI9n8/MhLMTq7bhMav\\nHI7XHcR5+JkTARbjBr86vEJjnfHHVw62NqgHA30VFjYbJE2B40G/WqRkq9uZrOzC\\n5Xvwp9alI3Eq7yWTULTXtuC/JZAOrf4lT4X/NYNzwIHSG8+lrMUhXQGOCWv9Zxbs\\nyp0A24/1PsMyYN75Dj+cxUPzakcJ6kIaePvF9uRBJagaboOMxD2x1Zq58uAshF+K\\nODtrcpTkN46E2Ez2cVUmsoRjDt/VLiQeehfwRYt1Vl2jCVkKHvabuqKVWnlL83vr\\nEwSjD6E/7PgGNvYZGM/+sfE7fX7jS78Vds0oZrNRCQKBgQDVrO3z2+QZu1tmr+QJ\\n2H+9Pozf/q3tI+Kjf8Z03y1INGC0ljIohJxGlD6R7Oqc3S5PHEgC8Lj6UJdX7A42\\n/P8kuIQ87dP6fS0aeuVsM2yS8gMr2njMwuEHPwKc6LkdsWvZQP5KvjX58F0TY26u\\nRfjBPlfMjZ3fg2evj6fJGyhoqwKBgQC+3UdbDFye6TnegHIUaSbWFsaMKW4SS2tF\\nNfJUmCvWEWoSmdcyPo8TNKo5929qAkEmJgALESNwU0XwpBBsgAvIEwmx7rY9Dba9\\njg+5lDXc7F5bWRrzJ26MSXAzUOdMx0jk919twendJH1x4x9RX4S7NbVw99QWcqxc\\n5SmZ0m7uAwKBgHYup43xWUBCOFObhW1MqZpqNlDN9DTtXDVCPun1Zn5BOhun1yZB\\n8o23AMSFXV5Vl396DPpTWnxYhtzCWzpexF/zDnEEufIZuhCjWLF3392Grepbc+UN\\nBJmVaESRE5Iwx43qPLvqaMBNCa3nmRga63M2oCkrSt6NN5QKyKqassbxAoGAKyGi\\nMGcYvyiBVVC9dvNUPWkkMSRjpWq5sQhB3PAOZ+/DgrSVNtuARZzPIw5RdSlRQ6eu\\nttGGqqmG0pygwYQmJW538Ge7cwyYUTm7P/rIOUaJBCecuXodt0IZQt9zhZw7UtK8\\nE/eQO9M1LflfaGoneo7mk8LNgM0lOlDnF8XAH7UCgYEAmeXG+rqA0MLUtucG3xaV\\nkU2ij2LLUeBBEtywi+UF9nRLtrbpU/js8cIN6mXXfkCUfWUUP3ey7q92Eyhx5DDN\\nqZ10H/AVrkluMHuNAUJDctO9GPit32z7PeDuO/AZKbufYgIpqkfShsXZ3kkEIfiC\\nH7r1qakFeFiVwF2Ewm1MbdE=\\n-----END PRIVATE KEY-----\\n","client_email": "gcptesting2@onepanelio.iam.gserviceaccount.com","client_id": "109315516570847019201","auth_uri": "https://accounts.google.com/o/oauth2/auth","token_uri": "https://oauth2.googleapis.com/token","auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs","client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/gcptesting2%40onepanelio.iam.gserviceaccount.com"}')
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

    def build_full_cloud_specific_url(self, path):
        return self.build_full_gcs_url(path)

    def get_dataset_bucket_name(self):
        return os.getenv('DATASET_BUCKET', 'onepanel-datasets')

    def upload_dir(self, dataset_directory, gcs_directory, exclude=''):
        bucket = self.storageClient.get_bucket(self.get_dataset_bucket_name())
        dataset_directory_for_upload = dataset_directory.rstrip("/")

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
                    root_path_for_gcp = root_path_for_gcp.replace("\\","/")
                # We want to set the specified directory as the "current directory" or context of upload.
                # This is to avoid uploading the entire absolute path.
                root_path_for_gcp = root_path_for_gcp.replace(dataset_directory_for_upload,"",1)

                file_path = os.path.join(root, filename)

                # This will be empty for top-level walking, but not sub-directories
                if not root_path_for_gcp:
                    upload_path = "/".join([gcs_directory, filename])
                else:
                    upload_path = "".join([gcs_directory, root_path_for_gcp])
                    upload_path = "/".join([upload_path, filename])
                print("Uploading {file}...".format(file=file_path))
                blob = bucket.blob(upload_path)
                blob.upload_from_filename(file_path)
                print("Uploaded {file}".format(file=file_path))
        return 0

    def download_all(self, dataset_directory, cs_directory):
        """
        This can be run in the background via 'datasets-background-download' CLI command.
        :param dataset_directory: string
        :param cs_directory: string
        :return: int
        """
        bucket = self.storageClient.get_bucket(self.get_dataset_bucket_name())
        blobs = bucket.list_blobs(prefix=cs_directory)
        for blob in blobs:
            blob = bucket.blob(blob.name)
            download_context = blob.name.replace(cs_directory,"",1).lstrip("/")
            if platform.system() is 'Windows':
                download_context = download_context.replace("/", "\\")
            download_path = os.path.sep.join([dataset_directory,download_context])
            # Ensure the parent directories exist before downloading
            if platform.system() is 'Windows':
                separator_before_file = download_path.rfind("\\")
            else:
                separator_before_file = download_path.rfind("/")
            dir_path = download_path[:separator_before_file]
            if not os.path.exists(dir_path):
                os.makedirs(dir_path,exist_ok=True)
            blob.download_to_filename(download_path)
            if self.suppress_output is False:
                print('File {} downloaded to {}.'.format(
                    download_context,
                    download_path))
        return 0

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

    # todo support running in the background
    def download(self, to_dir, cloud_provider_full_path_to_file):
        bucket = self.storageClient.get_bucket(self.get_dataset_bucket_name())
        blob = bucket.blob(cloud_provider_full_path_to_file)
        if not blob.exists():
            print("File does not exist.")
            return -1
        file_to_download_idx = blob.name.rfind("/")
        download_context = blob.name[file_to_download_idx:].lstrip("/")
        if platform.system() is 'Windows':
            download_context = download_context.replace("/", "\\")
        download_path = os.path.sep.join([to_dir, download_context])
        blob.download_to_filename(download_path)
        if self.suppress_output is False:
            print('File {} downloaded to {}.'.format(
                download_context,
                download_path))
        return 0

    def check_cloud_path_for_files(self, full_cloud_path='', recursive=True):
        # We have a collision between AWS CLI code and the SDK code of GCP.
        # For AWS, this same function passes in the entire path, such as "s3://<bucket>/<project>/<etc>"
        # The reason for this path is because the AWS CLI needs this notation, so that it can download the files.
        # The GCP SDK does NOT need this, since the bucket object is retrieved from the client, and that
        # already has the "gs://<bucket>" portion of the path.
        # If "gsutil" was compatible with Python 3.x, we could use the same path as for AWS.
        # But it's not, so we have to remove the "gs://<dataset>" prefix, since it'll be passed in.
        path_without_prefix = full_cloud_path.replace(self.build_full_gcs_url(""),"",1)
        if path_without_prefix == '':
            ret_val = {'data': None, 'code': -1, 'msg': 'Need the full cloud path passed in.'}
            return ret_val
        bucket = self.storageClient.get_bucket(self.get_dataset_bucket_name())
        # Another collision between AWS CLI code and the SDK code of GCP.
        # AWSCLI would get summary information, regardless if the path to a file was passed in
        # or a directory.
        # GCP SDK has to do this differently, hence we rely that "recursive" means a directory
        if recursive:
            blobs = bucket.list_blobs(prefix=path_without_prefix)
            # Can't get initialization until you try to iterate through the blobs.
            num_files = 0
            for blob in blobs:
                num_files = num_files + 1
            ret_val = {'data': num_files, 'code': 0, 'msg': 'Total files found.'}
        else:
            blob = bucket.blob(path_without_prefix)
            if blob.exists():
                data = 1
            else:
                data = 0
            ret_val = {'data': data, 'code': 0, 'msg': 'Total files found.'}

        # # todo support recursive
        # recursive_arg = ''
        # if recursive:
        #     recursive_arg = '--recursive'

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