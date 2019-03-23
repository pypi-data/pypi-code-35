from .tripdetail import TripDetail

class Trip:
    def __init__(self, json):
        self.id = 0
        self.ride_number = None
        self.equipmentId = None
        self.distance = 0
        self.start = None
        self.end = None
        self.type = None
        self.parse_json(json)
    
    def parse_json(self, json):
        self.id = json['Id']
        self.ride_number = json['RideNumber']
        self.equipmentId = json['EquipmentId']
        self.distance = json['Distance']
        self.type = json['RideType']
        self.start = TripDetail(json['From'])
        self.end = TripDetail(json['To'])

    def __str__(self):
        return f"{self.id}: {self.ride_number} - {self.start}"

