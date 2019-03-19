from rover_position_rjg.data.flags import Flags
from rover_position_rjg.data.vector import Vector
from rover_position_rjg.data.data import Data
from rover_position_rjg.json_aware.json_aware import JsonAware


class NineDoFData(JsonAware['NineDoFData']):
    @staticmethod
    def zero() -> 'NineDoFData':
        # Don't use the same object for acc/gyro and mag as it means editing one vector edits all of them.
        return NineDoFData(Data(Vector.zero(), 0), Data(Vector.zero(), 0), Data(Vector.zero(), 0), Data(0, 0))

    @staticmethod
    def one() -> 'NineDoFData':
        # Don't use the same object for acc/gyro and mag as it means editing one vector edits all of them.
        return NineDoFData(Data(Vector.one(), 0), Data(Vector.one(), 0), Data(Vector.one(), 0), Data(1, 0))

    def __init__(self,
                 acceleration: Data[Vector],
                 angular_velocity: Data[Vector],
                 magnetic_field: Data[Vector],
                 temperature: Data[float],
                 status: Flags = None):
        if not status:
            status = Flags()
        self.acceleration = acceleration
        self.angular_velocity = angular_velocity
        self.magnetic_field = magnetic_field
        self.temperature = temperature
        self.status = status

    def __eq__(self, other):
        if isinstance(other, NineDoFData):
            return self.acceleration == other.acceleration and \
                   self.angular_velocity == other.angular_velocity and \
                   self.magnetic_field == other.magnetic_field and \
                   self.temperature == other.temperature and \
                   self.status == other.status
        return False

    def __add__(self, other):
        acc = Data(self.acceleration.value + other.acceleration.value, self.acceleration.timestamp)
        av = Data(self.angular_velocity.value + other.angular_velocity.value, self.angular_velocity.timestamp)
        mag = Data(self.magnetic_field.value + other.magnetic_field.value, self.magnetic_field.timestamp)
        temp = Data(self.temperature.value + other.temperature.value, self.temperature.timestamp)
        return NineDoFData(acc, av, mag, temp, self.status)

    def __sub__(self, other):
        acc = Data(self.acceleration.value - other.acceleration.value, self.acceleration.timestamp)
        av = Data(self.angular_velocity.value - other.angular_velocity.value, self.angular_velocity.timestamp)
        mag = Data(self.magnetic_field.value - other.magnetic_field.value, self.magnetic_field.timestamp)
        temp = Data(self.temperature.value - other.temperature.value, self.temperature.timestamp)
        return NineDoFData(acc, av, mag, temp, self.status)

    def __mul__(self, other: float):
        acc = Data(self.acceleration.value * other, self.acceleration.timestamp)
        av = Data(self.angular_velocity.value * other, self.angular_velocity.timestamp)
        mag = Data(self.magnetic_field.value * other, self.magnetic_field.timestamp)
        temp = Data(self.temperature.value * other, self.temperature.timestamp)
        return NineDoFData(acc, av, mag, temp, self.status)

    def __truediv__(self, other: float):
        acc = Data(self.acceleration.value / other, self.acceleration.timestamp)
        av = Data(self.angular_velocity.value / other, self.angular_velocity.timestamp)
        mag = Data(self.magnetic_field.value / other, self.magnetic_field.timestamp)
        temp = Data(self.temperature.value / other, self.temperature.timestamp)
        return NineDoFData(acc, av, mag, temp, self.status)

    def scale(self, other):
        """Scales each element of this vector by the corresponding element of other."""
        acc = Data(self.acceleration.value.scale(other.acceleration.value), self.acceleration.timestamp)
        av = Data(self.angular_velocity.value.scale(other.angular_velocity.value), self.angular_velocity.timestamp)
        mag = Data(self.magnetic_field.value.scale(other.magnetic_field.value), self.magnetic_field.timestamp)
        temp = Data(self.temperature.value * other.temperature.value, self.temperature.timestamp)
        return NineDoFData(acc, av, mag, temp, self.status)

    def to_json(self) -> str:
        return '{{\n  "acceleration":{},\n  "angular_velocity":{},\n  "magnetic_field":{},\n  "temperature":{},\n  "status":"{}"\n}}'\
            .format(self.acceleration.to_json(), self.angular_velocity.to_json(), self.magnetic_field.to_json(), self.temperature.to_json(), self.status)

    @staticmethod
    def from_json(obj: dict) -> 'NineDoFData':
        acc = Data.from_json(obj['acceleration'], Vector.from_json)
        av = Data.from_json(obj['angular_velocity'], Vector.from_json)
        mag = Data.from_json(obj['magnetic_field'], Vector.from_json)
        temp = Data.from_json(obj['temperature'])
        if 'status' in obj:
            status = int(obj['status'], 0)
        else:
            status = 0
        return NineDoFData(acc, av, mag, temp, Flags(status))
