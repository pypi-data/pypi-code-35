from .TimestampMap import *


def create_flights(datafile: str, config: Config, min_timestamp: int = 0, max_timestamp: int = 9000000000) \
        -> List[Flight]:
    """
    create a list of flights from an IEFISBB.DAT datafile
    :param datafile:
    :param config:
    :param min_timestamp:
    :param max_timestamp:
    :return: List[Flight]
    """

    flights: List[Flight] = []

    with open(datafile, 'rb') as filepointer:
        packet_stream = MglPacketStream(filepointer, min_timestamp, max_timestamp)

        try:
            while True:
                message = find_message(packet_stream, config)
                flight = Flight(message, config)
                try:
                    while True:
                        try:
                            message = find_message(packet_stream, config)
                            flight.add_message(message)
                        except NotAMessage:
                            pass
                        except struct.error:
                            pass
                except NotPartOfFlightException:
                    pass
                finally:
                    flights.append(flight)
        except EndOfFile:
            pass

    timestamp_map = TimestampMap()
    timestamp_map.build_from_flights(flights)

    for flight in flights:
        flight.timestamp_map = timestamp_map

    return flights
