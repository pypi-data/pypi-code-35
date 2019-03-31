import json
import google.oauth2
from google.cloud import storage
from injector import inject

from gumo.core.injector import injector
from gumo.core.domain.configuration import GumoConfiguration


class CredentialManager:
    _credential = None

    @classmethod
    def get_credential(cls):
        if cls._credential:
            return cls._credential

        cls._credential = injector.get(cls).build_credential_from_storage()
        return cls._credential

    @inject
    def __init__(
            self,
            gumo_configuration: GumoConfiguration,
    ):
        self._gumo_configuration = gumo_configuration
        self._credential_config = self._gumo_configuration.service_account_credential_config

    def build_credential_from_storage(self):
        if not self._credential_config.enabled:
            raise RuntimeError(f'ServiceAccount Credential Config disabled.')

        return google.oauth2.service_account.Credentials.from_service_account_info(
            info=self._get_content()
        )

    def _get_content(self):
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name=self._credential_config.bucket_name)
        blob = bucket.blob(blob_name=self._credential_config.blob_path)
        content = blob.download_as_string(client=storage_client)

        return json.loads(content)


def get_credential():
    return CredentialManager.get_credential()
