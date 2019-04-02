import json
import os

from google.cloud.exceptions import NotFound, GoogleCloudError
from google.cloud import storage
from google.oauth2 import service_account

from onepanel.utilities.gcp_cs.authentication import Provider
from onepanel.utilities.gcp_utility import GCPUtility


class Wrapper:
    @staticmethod
    def is_error_expired_token(error):
        """
        :param error:
        :type error ClientError
        :return:
        """

        return error.response['Error']['Code'] == 'ExpiredToken'

    def __init__(self, bucket_name=None, credentials_provider=None, retry=3):
        """
        :param bucket_name: GCP CS Bucket name
        :param credentials_provider: Provides credentials for requests.
        :type credentials_provider: onepanel.utilities.gcp_cs.authentication.Provider
        """
        if bucket_name is None:
            bucket_name = os.getenv('DATASET_BUCKET', 'onepanel-datasets')

        if credentials_provider is None:
            credentials_provider = Provider()

        self.bucket_name = bucket_name
        self.credentials_provider = credentials_provider
        self.gcp_cs = None
        self.reset_client()
        self.retry = retry
        self.retries = 0

    def create_client(self):
        # todo remove hard-coded credentials
        json_str = '{"type": "service_account","project_id": "onepanelio","private_key_id": "2eff59c1256e14e88dda2eb97dd9bc0c8f11db96","private_key": "-----BEGIN PRIVATE KEY-----\\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCfTwpzXYDAnwlM\\nPiNWAk+WwPfufWtIMRfrt1QuJHnukUXwBk0mtLQHleTcI7ny4rO8Dbv5RIbbWOBD\\nv1fj16BgAtUMiDTocgMBHrngWyBUv6DO5IVEdgZGlZFiO672g7cPV9/A2JqFgg1g\\nXA5fA5CKB/JIjNo9ENwqEwp553zGBRKBXCL2FQB7Yy7SzmUipze1oE++KCWSWNUC\\nGF508cB2TT8hRvCs6UCldBsZD152dBmoeEVU2P5C1dgcZfDgqm5YXcbCaq+N/ICW\\n2PMe3073aY3WY8jPf1sN55epA6a57DDfDN2Fv7PcT8HjU5SpcQmNt/CBTjD8/XY9\\nsQciQjQBAgMBAAECggEABigN0ADbCuvvy2HTXRg1xIOskSuI9n8/MhLMTq7bhMav\\nHI7XHcR5+JkTARbjBr86vEJjnfHHVw62NqgHA30VFjYbJE2B40G/WqRkq9uZrOzC\\n5Xvwp9alI3Eq7yWTULTXtuC/JZAOrf4lT4X/NYNzwIHSG8+lrMUhXQGOCWv9Zxbs\\nyp0A24/1PsMyYN75Dj+cxUPzakcJ6kIaePvF9uRBJagaboOMxD2x1Zq58uAshF+K\\nODtrcpTkN46E2Ez2cVUmsoRjDt/VLiQeehfwRYt1Vl2jCVkKHvabuqKVWnlL83vr\\nEwSjD6E/7PgGNvYZGM/+sfE7fX7jS78Vds0oZrNRCQKBgQDVrO3z2+QZu1tmr+QJ\\n2H+9Pozf/q3tI+Kjf8Z03y1INGC0ljIohJxGlD6R7Oqc3S5PHEgC8Lj6UJdX7A42\\n/P8kuIQ87dP6fS0aeuVsM2yS8gMr2njMwuEHPwKc6LkdsWvZQP5KvjX58F0TY26u\\nRfjBPlfMjZ3fg2evj6fJGyhoqwKBgQC+3UdbDFye6TnegHIUaSbWFsaMKW4SS2tF\\nNfJUmCvWEWoSmdcyPo8TNKo5929qAkEmJgALESNwU0XwpBBsgAvIEwmx7rY9Dba9\\njg+5lDXc7F5bWRrzJ26MSXAzUOdMx0jk919twendJH1x4x9RX4S7NbVw99QWcqxc\\n5SmZ0m7uAwKBgHYup43xWUBCOFObhW1MqZpqNlDN9DTtXDVCPun1Zn5BOhun1yZB\\n8o23AMSFXV5Vl396DPpTWnxYhtzCWzpexF/zDnEEufIZuhCjWLF3392Grepbc+UN\\nBJmVaESRE5Iwx43qPLvqaMBNCa3nmRga63M2oCkrSt6NN5QKyKqassbxAoGAKyGi\\nMGcYvyiBVVC9dvNUPWkkMSRjpWq5sQhB3PAOZ+/DgrSVNtuARZzPIw5RdSlRQ6eu\\nttGGqqmG0pygwYQmJW538Ge7cwyYUTm7P/rIOUaJBCecuXodt0IZQt9zhZw7UtK8\\nE/eQO9M1LflfaGoneo7mk8LNgM0lOlDnF8XAH7UCgYEAmeXG+rqA0MLUtucG3xaV\\nkU2ij2LLUeBBEtywi+UF9nRLtrbpU/js8cIN6mXXfkCUfWUUP3ey7q92Eyhx5DDN\\nqZ10H/AVrkluMHuNAUJDctO9GPit32z7PeDuO/AZKbufYgIpqkfShsXZ3kkEIfiC\\nH7r1qakFeFiVwF2Ewm1MbdE=\\n-----END PRIVATE KEY-----\\n","client_email": "gcptesting2@onepanelio.iam.gserviceaccount.com","client_id": "109315516570847019201","auth_uri": "https://accounts.google.com/o/oauth2/auth","token_uri": "https://oauth2.googleapis.com/token","auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs","client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/gcptesting2%40onepanelio.iam.gserviceaccount.com"}'
        if not json_str:
            print("Google credentials cannot be empty! Check the environment variable: {env_var}.".format(
                env_var='GOOGLE_APPLICATION_CREDENTIALS_JSON_STR'))
            exit(-1)

        service_account_info = json.loads(json_str)
        credentials = service_account.Credentials.from_service_account_info(service_account_info)
        storage_client = storage.Client("onepanelio", credentials)
        if not self.credentials_provider.loads_credentials():
            return storage_client

        credentials = self.credentials_provider.credentials()

        return storage_client

    def reset_client(self):
        self.gcp_cs = self.create_client()

    def list_files(self, prefix):
        files = {}
        gcp_utility = GCPUtility()
        bucket = gcp_utility.storageClient.get_bucket(gcp_utility.get_dataset_bucket_name())
        blobs = bucket.list_blobs(prefix=prefix)
        for blob in blobs:
            files[blob.name] = blob

        # Skip the file that has the same name as the prefix.
        if prefix in files:
            del files[prefix]

        self.retries = 0
        return files

    def upload_file(self, filepath, key):
        # Normalize s3 path if we're on windows
        key = key.replace('\\', '/')

        try:
            gcp_utility = GCPUtility()
            bucket = gcp_utility.storageClient.get_bucket(gcp_utility.get_dataset_bucket_name())
            blob = bucket.blob(key)
            blob.upload_from_filename(filepath)
            self.retries = 0
            return True
        except GoogleCloudError:
            if self.retries < self.retry:
                self.retries += 1
                self.reset_client()
                return self.upload_file(filepath, key)

            raise
        except FileNotFoundError as fileNotFoundError:
            # Do nothing
            return

    def download_file(self, local_path, key):
        gcp_utility = GCPUtility()
        bucket = gcp_utility.storageClient.get_bucket(gcp_utility.get_dataset_bucket_name())
        blob = bucket.blob(key)
        try:
            # Create the directory locally if it doesn't exist yet.
            dirname = os.path.dirname(local_path)
            os.makedirs(dirname, exist_ok=True)
            blob.download_to_filename(local_path)
        except NotFound:
            if self.retries < self.retry:
                self.retries += 1
                self.reset_client()
                return self.download_file(local_path, key)

            raise

    def delete_file(self, key):
        key = key.replace('\\', '/')

        try:
            gcp_utility = GCPUtility()
            bucket = gcp_utility.storageClient.get_bucket(gcp_utility.get_dataset_bucket_name())
            bucket.delete_blob(blob_name=key)

            self.retries = 0
            return True
        except NotFound:
            if self.retries < self.retry:
                self.retries += 1
                self.reset_client()
                return self.delete_file(key)

            raise

    def copy_file(self, source_key, destination_key):
        # Normalize s3 path if we're on windows
        source_key = source_key.replace('\\', '/')
        destination_key = destination_key.replace('\\', '/')
        gcp_utility = GCPUtility()
        bucket = gcp_utility.storageClient.get_bucket(gcp_utility.get_dataset_bucket_name())
        blob = bucket.blob(source_key)
        copied_blob = bucket.copy_blob(blob=blob, destination_bucket=bucket, new_name=destination_key)

    def move_file(self, source_key, destination_key):
        # We do a try here in case copy fails, in which case we don't try delete.
        try:
            self.copy_file(source_key, destination_key)
            self.delete_file(source_key)
        except BaseException:
            raise
