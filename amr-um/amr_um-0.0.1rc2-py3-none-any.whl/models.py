import attr


class DlmsWrapper:

    def __init__(self, source_wport, destination_wport, version=1):
        self.source_wport = source_wport
        self.destination_wport = destination_wport
        self.version = version

    def __repr__(self):
        return (
            f'{self.__class__.__name__}('
            f'source_wport={self.source_wport!r}, '
            f'destination_wport={self.destination_wport!r}, '
            f'version={self.version!r}'
            f')'
        )


class DlmsPushMessage:
    BASE_TOPIC = 'new_dlms_push_message'

    def __init__(self, payload: bytes, dlms_wrapper: DlmsWrapper,
                 transport: str, source_address: str, source_port: int,
                 application_context: str):
        self.payload = payload
        self.dlms_wrapper = dlms_wrapper
        self.transport = transport
        self.source_address = source_address
        self.source_port = source_port
        self.application_context = application_context

    def format_topic(self, schema_version):
        return (
            f'{self.BASE_TOPIC}'
            # f'.{self.source_address}'
            # f'.{self.source_port}'
            f'.{schema_version}'
        )

    def __repr__(self):
        return (
            f'{self.__class__.__name__}('
            f'payload={self.payload!r}, '
            f'dlms_wrapper={self.dlms_wrapper!r}, '
            f'transport={self.transport!r}, '
            f'source_address={self.source_address}, '
            f'source_port={self.source_port}, '
            f'application_context={self.application_context!r}'
            f')'
        )


class NewMeterReading:
    """
    New Meter Readings are meter readings for input in Utilitarian. They
    have not yet been validated and not all information is known about them.

    :param str meter: Meter Identification. Name of the
        meter.

    :param str series: Meter Reading Series name. What series on the meter this
        value refers to.
    :param str timestamp: Time when the value was registered.
    :param str value: Value

    """
    BASE_TOPIC = 'new_meter_reading'

    def __init__(self, meter, series, timestamp, value):

        self.meter = meter
        self.series = series
        self.timestamp = timestamp
        self.value = value

        # TODO: handle dots in series name.

    def format_topic(self, schema_version):
        return (
            f'{self.BASE_TOPIC}'
            f'.{self.meter}'
            f'.{self.series}'
            f'.{schema_version}'
        )

    def __repr__(self):
        return (
            f'{self.__class__.__name__}('
            f'meter={self.meter!r}, '
            f'series={self.series!r}, '
            f'timestamp={self.timestamp!r}, '
            f'value={self.value!r}'
            f')'
        )
