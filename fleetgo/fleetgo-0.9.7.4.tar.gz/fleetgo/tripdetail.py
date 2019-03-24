from .address import Address

class TripDetail:
    def __init__(self, json):
        self.date = None
        self.odometer = 0
        self.description = None
        self.address = None
        self.latitude = 0
        self.longitude = 0
        self.altitude = 0
        self.minutes_on_location = 0
        self.parse_json(json)
    
    def parse_json(self, json):
        import ciso8601

        self.odometer = json['Odometer']
        self.description = json['Description']
        self.latitude = json['Location']['Latitude']
        self.longitude = json['Location']['Longitude']
        self.altitude = json['Location']['Altitude']
        self.minutes_on_location = json['MinutesAtLocation']

        if json['DateTime'] is not None:
            self.date = ciso8601.parse_datetime(json['DateTime'])
        else:
            self.date = None

        self.address = Address(json['Address'])

    def __str__(self):
        return f"{self.address}"