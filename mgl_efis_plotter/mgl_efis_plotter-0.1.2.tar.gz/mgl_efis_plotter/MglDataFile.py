from .TimestampMap import *


def createFlights(datafile: str, config: Config, minTimestamp: int = 0, maxTimestamp: int = 9000000000) -> List[Flight]:
    """
    create a list of flights from an IEFISBB.DAT datafile
    :param datafile:
    :param config:
    :param minTimestamp:
    :param maxTimestamp:
    :return: List[Flight]
    """

    flights: List[Flight] = []

    with open(datafile, 'rb') as filePointer:
        packetStream = MglPacketStream(filePointer, minTimestamp, maxTimestamp)

    try:
        while True:
            message = findMessage(packetStream, config)
            flight = Flight(message, config)
            try:
                while True:
                    try:
                        message = findMessage(packetStream, config)
                        flight.addMessage(message)
                    except NotAMessage as e:
                        pass
                    except struct.error as e:
                        pass
            except NotPartOfFlightException as e:
                pass
            finally:
                flights.append(flight)
    except EndOfFile as e:
        pass

    timestampMap = TimestampMap()
    timestampMap.buildFromFlights(flights)

    for flight in flights:
        flight.timeStampMap = timestampMap

    return flights
