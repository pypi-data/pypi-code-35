from collections import OrderedDict
import csv

from .Message import *


class Flight(object):
    """
    Data from one flight, beginning at earliest_timestamp and ending at latest_timestamp
    """

    earliest_timestamp: int
    latest_timestamp: int

    messages: List[Message]
    timestamp_map: Dict

    earliest_datetime: datetime

    config: Config

    NEWFLIGHTDELTA: int

    def __init__(self, message: Message, config: Config):
        self.config = config
        self.NEWFLIGHTDELTA = self.config.new_flight_delta

        self.earliest_datetime = None

        self.earliest_timestamp = message.timestamp
        self.latest_timestamp = message.timestamp
        self.messages = [message]

    def add_message(self, message: Message) -> None:
        """
        add an EFIS message to a flight
        :param message:
        :return:
        :raise: NotPartOfFlightException when the message's timestamp is too long after previous message
        """
        if self.earliest_timestamp > message.timestamp:
            raise NotPartOfFlightException(
                'too early: {early} > {message}'.format(early=self.earliest_timestamp, message=message.timestamp))

        if message.timestamp > (self.latest_timestamp + self.NEWFLIGHTDELTA):
            raise NotPartOfFlightException(
                'too late: {message} > ({latest} + {delta})'.format(message=message.timestamp,
                                                                    latest=self.latest_timestamp,
                                                                    delta=self.NEWFLIGHTDELTA))

        self.messages.append(message)
        self.latest_timestamp = message.timestamp

    def get_plot_data(self, element: str) -> OrderedDict:
        """
        returns an OrderedDict of (minutes, datum) for use with Plot.
        Minutes starts at 0 at the beginning of the flight.
        Minutes is a float and there may be multiple data with the same minute value.
        :param element:
        :return:
        """
        dataset = OrderedDict()
        for message in self.messages:
            if hasattr(message.message_data, element):
                dataset[self._timestamp_to_minutes(message.timestamp)] = message.message_data.__getattribute__(element)
        return dataset

    def list_attributes(self) -> None:
        """
        prints a list of datum element names which can be used with get_plot_data() and list_data()
        :return:
        """
        attributes = self._get_attribute_list()
        for a in attributes:
            print(a)

    def _get_attribute_list(self) -> List[str]:
        attributes = []
        for message in self.messages:
            for attribute, value in message.message_data.__dict__.items():
                if isinstance(value, (int, float)) and 0 != value and attribute not in attributes:
                    attributes.append(attribute)
                elif ('cht' == attribute or 'egt' == attribute) and 0 != len(value) and attribute not in attributes:
                    attributes.append(attribute)
                elif 'date_time' == attribute:
                    attributes.append(attribute)
        attributes.sort()
        return attributes

    def list_data(self, element: str) -> Dict[str, List]:
        """
        returns a Dict of lists of {minutes, timestamp, datum} for use in a pandas DataFrame.
        Minutes starts at 0 at the beginning of the flight.
        There may be multiple data with the same minute and timestamp values.
        :param element:
        :return:
        """
        minutes = []
        timestamp = []
        data = []
        for message in self.messages:
            if hasattr(message.message_data, element):
                minutes.append(self._timestamp_to_minutes(message.timestamp))
                timestamp.append(message.timestamp)
                data.append(message.message_data.__getattribute__(element))
        return {
            'minutes': minutes,
            'timestamp': timestamp,
            element: data,
        }

    def save_csv(self, filename: str, elements: List[str] = None) -> None:
        """
        save a CSV file containing a list of data elements.
        :param filename:
        :param elements: list of elements; defaults to all elements
        :return:
        """
        if elements is None:
            elements = self._get_attribute_list()
        columns = ['minutes', 'timestamp']
        columns.extend(elements)

        with open(filename, 'w') as csvfile:
            csvwriter = csv.writer(csvfile)
            dictwriter = csv.DictWriter(csvfile, fieldnames=columns)
            csvwriter.writerow(columns)

            for message in self.messages:
                row = {}
                for element in elements:
                    if hasattr(message.message_data, element):
                        row[element] = message.message_data.__getattribute__(element)

                if 0 < len(row):
                    row['minutes'] = self._timestamp_to_minutes(message.timestamp)
                    row['timestamp'] = message.timestamp
                    dictwriter.writerow(row)

    def _timestamp_to_minutes(self, ts: int) -> float:
        return self._timestamp_to_seconds(ts) / 60.0

    def _timestamp_to_seconds(self, ts: int) -> int:
        if self.earliest_datetime is None:
            self.earliest_datetime = self.timestamp_map[self.earliest_timestamp]
        now = self.timestamp_map[ts]
        t = now - self.earliest_datetime
        return t.total_seconds()

    def title(self) -> str:
        """
        :return: a short title for use on graphs and reports
        """
        return 'Flight at {beginning}'.format(beginning=self._earliest_date_string())

    def _earliest_date_string(self) -> str:
        """
        return the earliest datetime as a string.
        usually that is the earliest timestamp but occasionally there was no RTC value for the timestamp,
        when that happens, find something else
        :return:
        """
        ds = self.timestamp_map[self.earliest_timestamp]
        if ds is not None:
            return ds

        earliest = min(list(self.timestamp_map.keys()))
        return self.timestamp_map[earliest]

    def _latest_date_string(self) -> str:
        """
        return the latest datetime as a string.
        usually that is the latest timestamp but occasionally there was no RTC value for the timestamp,
        when that happens, find something else
        :return:
        """
        ds = self.timestamp_map[self.latest_timestamp]
        if ds is not None:
            return ds

        latest = max(list(self.timestamp_map.keys()))
        return self.timestamp_map[latest]

    def __str__(self):
        t = 'Flight at {beginning} to {ending},   {qty:,d} messages'.format(
            beginning=self._earliest_date_string(),
            ending=self._latest_date_string(),
            qty=len(self.messages),
        )
        return t

    def _debug__str__(self):
        t = 'Flight at {beginning} to {ending}, {qty:5d} messages, timestamps {begin:,d} to {end:,d}'.format(
            beginning=self._earliest_date_string(),
            ending=self._latest_date_string(),
            qty=len(self.messages),
            begin=self.earliest_timestamp,
            end=self.latest_timestamp,
        )
        return t
