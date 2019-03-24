import sseclient
from .device import Device
from .trip import Trip
from .authentication import Authentication

import certifi


class API:

    def __init__(self, client_id, client_secret, username, password):
        self._client_id = client_id
        self._client_secret = client_secret
        self._username = username
        self._password = password
        self.authentication_info = None

    def logged_in(self):
        if (self.authentication_info is None):
            return False
        else:
            return self.authentication_info.is_valid()

    def login(self):
        import urllib3
        import json

        data_url = "https://api.fleetgo.com/api/session/login"

        body = {
            'client_id': self._client_id,
            'client_secret': self._client_secret,
            'username': self._username,
            'password': self._password
        }

        encoded_data = json.dumps(body).encode('utf-8')

        http = urllib3.PoolManager(
            cert_reqs='CERT_REQUIRED',
            ca_certs=certifi.where())

        response = http.request(
            'POST',
            data_url,
            body=encoded_data,
            headers={'Content-Type': 'application/json'}
        )

        response_data = json.loads(response.data.decode('utf-8'))
        self.authentication_info = Authentication()
        self.authentication_info.set_json(response_data)
        return self.logged_in()

    async def stream_devices(self, callback):
        import json
        import sseclient

        if (self.authentication_info is None or
                not self.authentication_info.is_valid()):
            return False

        data_url = "https://api.fleetgo.com/api/equipment/subscribe/?groupId=0&vehicleCategoryId=0&driverCategoryId=0"

        # self.urllib3_stream(data_url)
        response = self.requests_stream(data_url)
        client = sseclient.SSEClient(response)

        for event in client.events():
            data = json.loads(event.data)
            if (data != 'heartbeat'):
                devices = self.parse_devices(data)
                callback(devices)

    def parse_devices(self, json):
        """Parse result from API."""
        result = []

        for json_device in json:
            license_plate = json_device['EquipmentHeader']['SerialNumber']

            device = Device(self, license_plate)
            device.update_from_json(json_device)
            result.append(device)

        return result

    def requests_stream(self, url):
        import requests
        header = self.authentication_info.create_header()
        return requests.get(url, stream=True, headers=header)

    def urllib3_stream(self, url):
        import urllib3
        header = self.authentication_info.create_header()
        http = urllib3.PoolManager(
            cert_reqs='CERT_REQUIRED',
            ca_certs=certifi.where())

        return http.request(
            'GET',
            url,
            preload_content=False,
            headers=header)
