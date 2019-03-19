from json import dumps
from typing import TypeVar, Generic, Callable

from rover_position_rjg.json_aware.json_aware import JsonAware

TValue = TypeVar('TValue')


class Data(Generic[TValue], JsonAware['Data[TValue]']):
    """A piece of data that was defined at a particular point in time.
    Usually used for sensor data."""

    def __init__(self, value: TValue, timestamp):
        self.value = value
        self.timestamp = timestamp

    def __eq__(self, other):
        if type(other) != Data:
            return False
        return self.value == other.value and self.timestamp == other.timestamp

    def __repr__(self):
        return 'Data({}, {})'.format(self.value, self.timestamp)

    def to_json(self) -> str:
        if isinstance(self.value, JsonAware):
            json = self.value.to_json()
        else:
            json = dumps(self.value)
        return '{{"value":{}, "timestamp":{}}}'.format(json, self.timestamp)

    @staticmethod
    def from_json(obj: dict, value_parser: Callable[[dict], 'TValue'] = None) -> 'Data[TValue]':
        timestamp = obj['timestamp']
        value = obj['value']
        if value_parser:
            return Data(value_parser(value), timestamp)
        else:
            return Data(value, timestamp)
