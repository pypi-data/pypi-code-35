from .trip import Trip
from .address import Address


class Device:
    """Entity used to store device information."""

    def __init__(self, data, license_plate):
        """Initialize a FleetGO device, also a vehicle."""
        self._data = data

        self.attributes = {}
        self.license_plate = license_plate

        self.identifier = None
        self.make = None
        self.model = None
        self.active = False
        self.odo = 0
        self.latitude = 0
        self.longitude = 0
        self.altitude = 0
        self.speed = 0
        self.last_seen = None
        self.equipment_id = None

        self.malfunction_light = False
        self.fuel_level = -1
        self.coolant_temperature = 0
        self.power_voltage = 0

        self.current_maximum_speed = 0
        self.current_address = None

    @property
    def plate_as_id(self):
        """Format the license plate so it can be used as identifier."""
        return self.license_plate.replace('-', '')

    @property
    def state_attributes(self):
        """Return all attributes of the vehicle."""

        address_attributes = None
        if (self.current_address is not None):
            address_attributes = self.current_address.state_attributes()

        return {
            'id': self.identifier,
            'make': self.make,
            'model': self.model,
            'license_plate': self.license_plate,
            'active': self.active,
            'odo': self.odo,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'altitude': self.altitude,
            'speed': self.speed,
            'last_seen': self.last_seen,
            'friendly_name': self.license_plate,
            'equipment_id': self.equipment_id,
            'fuel_level': self.fuel_level,
            'malfunction_light': self.malfunction_light,
            'coolant_temperature': self.coolant_temperature,
            'power_voltage': self.power_voltage,
            'current_max_speed': self.current_maximum_speed,
            'current_address': address_attributes
        }

    def get_trips(self, authentication_info, start, end):
        """Get trips for this device between start and end."""
        import requests

        if (authentication_info is None or
                not authentication_info.is_valid()):
            return []

        data_url = "https://api.fleetgo.com/api/trips/GetTrips"
        query = f"?equipmentId={self.identifier}&from={start}&to={end}&extendedInfo=True"
        header = authentication_info.create_header()
        response = requests.get(data_url + query, headers=header)
        trips = response.json()

        result = []
        for trip_json in trips:
            trip = Trip(trip_json)
            result.append(trip)
        return result

    def get_extra_vehicle_info(self, authentication_info):
        """Get extra data from the API."""
        import requests

        base_url = "https://secure.fleetgo.com/GenericServiceJSONP.ashx"
        query = "?f=CheckExtraVehicleInfo" \
                "&token={token}" \
                "&equipmentId={identifier}" \
                "&lastHash=null&padding=false"

        parameters = {
            'token': authentication_info.access_token,
            'identifier': str(self.identifier)
        }

        response = requests.get(base_url + query.format(**parameters))
        json = response.json()

        self.malfunction_light = json['MalfunctionIndicatorLight']
        self.fuel_level = json['FuelLevel']
        self.coolant_temperature = json['EngineCoolantTemperature']
        self.power_voltage = json['PowerVoltage']

    def update_from_json(self, json_device):
        """Set all attributes based on API response."""
        self.identifier = json_device['Id']
        self.license_plate = json_device['EquipmentHeader']['SerialNumber']
        self.make = json_device['EquipmentHeader']['Make']
        self.model = json_device['EquipmentHeader']['Model']
        self.equipment_id = json_device['EquipmentHeader']['EquipmentID']
        self.active = json_device['EngineRunning']
        self.odo = json_device['Odometer']
        self.latitude = json_device['Location']['Latitude']
        self.longitude = json_device['Location']['Longitude']
        self.altitude = json_device['Location']['Altitude']
        self.speed = json_device['Speed']
        self.last_seen = json_device['Location']['DateTime']

    def get_map_details(self):
        import requests
        from .json_utils import JsonUtils

        if (self.latitude == 0 and self.longitude == 0):
            return

        url = "https://overpass-api.de/api/interpreter"
        query = f"[out:json][timeout:25];" \
                f"(way(around:25, {self.latitude}, {self.longitude})[maxspeed];" \
                f"node(around:100, {self.latitude}, {self.longitude})['addr:city'];" \
                f"is_in({self.latitude}, {self.longitude}); );" \
                "out;"

        response = requests.post(url, query)
        data = response.json()

        way = self.get_closest_way(data)
        country = self.get_country(data)
        self.current_maximum_speed = JsonUtils.get_attribute(
            way, ['tags', 'maxspeed'], 0)
        if self.current_maximum_speed == 'none':
            self.current_maximum_speed = 250

        street = self.get_closest_street(data)
        if (street is not None):
            self.current_address = Address(None)

            self.current_address.city = JsonUtils.get_attribute(
                street, ['tags', 'addr:city'], None)
            self.current_address.address = JsonUtils.get_attribute(
                street, ['tags', 'addr:street'], None)
            self.current_address.house_number = JsonUtils.get_attribute(
                street, ['tags', 'addr:housenumber'], None)
            self.current_address.postal_code = JsonUtils.get_attribute(
                street, ['tags', 'addr:postcode'], None)
            self.current_address.country = JsonUtils.get_attribute(
                street, ['tags', 'addr:country'], None)
        else:
            self.current_address = None

            if (way is not None):
                self.current_address = Address(None)
                self.current_address.address = JsonUtils.get_attribute(
                    way, ['tags', 'ref'], 0)

        if self.current_address is None or (self.current_address.country is None and country is not None):
            if self.current_address is None:
                self.current_address = Address(None)
            self.current_address.country = JsonUtils.get_attribute(
                country, ['tags', 'int_name'], None)

    def get_closest_way(self, json):
        for element in json['elements']:
            if (element['type'] == 'way'):
                return element

        return None

    def get_closest_street(self, json):
        result = []

        for element in json['elements']:
            if (element['type'] == 'node'):
                result.append(element)

        return self.get_closest_element(result)

    def get_country(self, json):
        lowest_admin = 999
        result = None

        for element in json['elements']:
            if (element['type'] == 'area' and 'admin_level' in element['tags'] and 'int_name' in element['tags']):
                if int(element['tags']['admin_level']) < lowest_admin:
                    lowest_admin = int(element['tags']['admin_level'])
                    result = element
        return result

    def get_closest_element(self, elements):
        import geopy.distance

        if (len(elements) > 0):
            min_distance = 99999999
            result = elements[0]

            for element in elements:
                d_position = (self.latitude, self.longitude)
                e_position = (element['lat'], element['lon'])
                distance = geopy.distance.vincenty(d_position, e_position).km

                if (distance < min_distance):
                    result = element
                    min_distance = distance

            return result
        else:
            return None
