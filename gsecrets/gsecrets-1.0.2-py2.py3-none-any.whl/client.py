import base64
import json
import os
import re
import warnings
import googleapiclient.discovery
from google.cloud import storage
from google.api_core.exceptions import NotFound
from .exceptions import (
    InsufficientConfiguration,
    SecretNotFound,
)

# Suppress this warning as this tool is intended to be authenticated
# using user credentials. May revisit this decision in the future.
warnings.filterwarnings("ignore", "Your application has authenticated using end user credentials")

class Client(object):

    project_id = None
    location = None
    keyring = None
    key = None
    bucket_name = None
    bucket = None
    resource = None

    def __init__(self, vault_location):

        # TODO: add error handling for bad `vault_location` formatting
        pattern = "(.+)\/(.+)"
        matches = re.search(pattern, vault_location)
        self.project_id = matches.group(1)
        self.bucket_name = matches.group(2)

        self.storage_client = storage.Client(project=self.project_id)
        self.bucket = self.storage_client.bucket(self.bucket_name)
        self.pull_keyring_configuration()

        self.resource = "projects/{}/locations/{}/keyRings/{}/cryptoKeys/{}".format(
            self.project_id,
            self.location,
            self.keyring,
            self.key
        )

    def pull_keyring_configuration(self):
        # TODO: error handling if this file is missing or badly configured
        path = "keyring.json"
        blob = self.bucket.blob(path)
        keyring_configuration = blob.download_as_string()
        keyring_configuration = json.loads(keyring_configuration)
        self.location = keyring_configuration["location"]
        self.keyring = keyring_configuration["keyring"]
        self.key = keyring_configuration["key"]

    def put(self, path, content, replace=False):
        """Put a secret with value `content` at `path`

        Optional arguments:

            replace: if set to `False`, will do a dict.update if an object already
                     exists in GCS. If `True`, completely replaces the object.

        Examples:

            put("slack/token", "AABBBCCC")

        Replace an entire dictionary

            put("manifests/admiral/env.json", {airflow_fernet_key: "AAABBBCCC"}, replace=True)


        """

        dictionary_mode = path.endswith(".json")

        # One other way to enter dictionary-mode, which is the dictionary-key syntax.
        # If the path ends with ".json.KEY", replace a single key in the dictionary.
        #
        # e.g. 
        #   
        #   path=project/bucket/env.json.key 
        #   content=value
        #
        pattern = "(.+\.json)\.(.+)$"
        matches = re.search(pattern, path)
        if matches:
            dictionary_mode = True
            path = matches.group(1)
            key = matches.group(2)
            content = json.dumps({key: content})
            replace = False

        if dictionary_mode:
            try:
                existing_secret = self.get(path)
            except SecretNotFound:
                existing_secret = {}

            if type(content) is not dict:
                new_secret = json.loads(content)

            if replace:
                content = json.dumps(new_secret)
            else:
                existing_secret.update(new_secret)
                content = json.dumps(existing_secret)

        kms_client = googleapiclient.discovery.build('cloudkms','v1')
        crypto_keys = kms_client.projects().locations().keyRings().cryptoKeys()
        encoded = base64.b64encode(content.encode('utf-8'))
        request = crypto_keys.encrypt(
            name=self.resource,
            body={
                'plaintext': encoded.decode('utf-8')
            }
        )
        response = request.execute()

        ciphertext = response['ciphertext']

        blob = self.bucket.blob(path)
        blob.upload_from_string(ciphertext)


    def get(self, path):
        """Retrieve a secret

        Examples:

            get("slack/token") -> "AAABBBCCC"
            
        Automatically parse json if the path ends with `.json`:

            get("manifests/admiral/env.json") -> "{'key': AAABBBCCC}"

        Retrieve a single value from a json file:
        
            get("manifests/admiral/env.json.key") -> "AAABBBCCC"

        """

        # Check if this is a json key path
        pattern = "(.+\.json)\.(.+)$"
        matches = re.search(pattern, path)
        json_extract_mode = False
        if matches:
            json_extract_mode = True
            path = matches.group(1)
            key = matches.group(2)

        blob = self.bucket.blob(path)

        try:
            ciphertext = blob.download_as_string()
        except NotFound:
            raise SecretNotFound()

        kms_client = googleapiclient.discovery.build('cloudkms','v1')
        crypto_keys = kms_client.projects().locations().keyRings().cryptoKeys()
        request = crypto_keys.decrypt(
            name=self.resource,
            body={
                'ciphertext': ciphertext.decode('utf-8')
            }
        )
        response = request.execute()
        plaintext = base64.b64decode(response['plaintext'].encode('utf-8'))

        if json_extract_mode:
            return json.loads(plaintext).get(key)

        if path.endswith(".json"):
            return json.loads(plaintext)

        return plaintext




