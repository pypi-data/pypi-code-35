from .device import Device
from .trip import Trip
from .authentication import Authentication


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
        import requests

        data_url = "https://api.fleetgo.com/api/session/login"

        body = {
            'client_id': self._client_id,
            'client_secret': self._client_secret,
            'username': self._username,
            'password': self._password
        }

        response = requests.post(data_url, json=body)

        self.authentication_info = Authentication()
        self.authentication_info.set_json(response.json())
        return self.logged_in()

    def stream_devices(self, callback):
        import json
        import certifi
        import urllib3
        import sseclient

        if (self.authentication_info is None or
                not self.authentication_info.is_valid()):
            return False

        data_url = "https://api.fleetgo.com/api/equipment/subscribe/?groupId=0&vehicleCategoryId=0&driverCategoryId=0"

        header = self.authentication_info.create_header()
        http = urllib3.PoolManager(
            cert_reqs='CERT_REQUIRED',
            ca_certs=certifi.where())

        response = http.request(
            'GET',
            data_url,
            preload_content=False,
            headers=header)

        client = sseclient.SSEClient(response)
        for event in client.events():
            data = json.loads(event.data)
            if (data != 'heartbeat'):
                devices = self.parse_devices(data)
                callback(devices)

    def get_devices(self):
        import requests

        if (self.authentication_info is None or
                not self.authentication_info.is_valid()):
            return []

        data_url = "https://api.fleetgo.com/api/equipment/Getfleet"
        query = "?groupId=0&hasDeviceOnly=false"

        header = self.authentication_info.create_header()
        response = requests.get(data_url + query, headers=header)
        data = response.json()
        return self.parse_devices(data)

    def parse_devices(self, json):
        """Parse result from API."""
        result = []

        for json_device in json:
            license_plate = json_device['EquipmentHeader']['SerialNumber']

            device = Device(self, license_plate)
            device.update_from_json(json_device)
            result.append(device)

        return result
