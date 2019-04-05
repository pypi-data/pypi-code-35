from .Flight import *


class TimestampMap(dict):
    """
    map timestamps from the MGL iEFIS records to datetime values, using the real time clock (RTC) from the
    PrimaryFlight records
    """
    lastValue = None
    minKey = 99999999

    def __getitem__(self, item):
        if item < self.minKey:
            raise KeyError
        if item in self.keys():
            found_value = super().__getitem__(item)
            if found_value is None:
                return self.__getitem__(item - 1)
            self.lastValue = found_value
        return self.lastValue

    def __setitem__(self, key, value):
        if key < self.minKey:
            self.minKey = key
        return super().__setitem__(key, value)

    def build_from_flights(self, flights: List[Flight]) -> None:
        for flight in flights:
            for message in flight.messages:
                if isinstance(message.message_data, PrimaryFlight):
                    self[message.timestamp] = message.message_data.date_time
