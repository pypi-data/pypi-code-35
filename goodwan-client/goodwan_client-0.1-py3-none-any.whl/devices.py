"""
GoodWan client library: devices
"""
from goodwan_client.classes import Basic


class Device(Basic):
    name = "unknown"
    description = "unknown"
    id = -1

    def __init__(self, data):
        self.data = data["data"]
        self.data_ext = data["data_ext"]


class TempSensor(Device):
    name = "temp_sensor"
    description = "Датчик температуры"
    id = 101
    temp = None  # type: float

    def __init__(self, data):
        Device.__init__(self, data)
        self.temp = float(self.data)


class OrderButton(Device):
    name = "order_button"
    description = "Кнопка заказа"
    id = 102
    state = None  # type: int
    is_cancel = None  # type: bool
    is_order = None  # type: bool

    def __init__(self, data):
        Device.__init__(self, data)
        self.state = int(self.data)
        if self.state < 0 or self.state > 1:
            raise ValueError("Wrong order button state value {}".format(state))
        self.is_cancel = bool(self.state)
        self.is_order = not self.is_cancel


class PulseSensor(Device):
    name = "pulse_sensor"
    description = "Счетчик импульсов (универсальный ЖКХ счетчик)"
    id = 103
    pulse1 = None  # type: float
    pulse2 = None  # type: float

    def __init__(self, data):
        Device.__init__(self, data)
        self.pulse = float(self.data)
        try:
            self.pulse2 = float(self.data_ext)
        except ValueError:
            pass


class LevelSensor(Device):
    name = "level_sensor"
    description = "Датчик уровня"
    id = 104
    level = None  # type: float

    def __init__(self, data):
        Device.__init__(self, data)
        self.level = float(self.data)


class VibrationSensor(Device):
    name = "vibration_sensor"
    description = "Датчик вибрации (датчик вибрации моста)"
    id = 105
    freq = None  # type: float
    amp = None  # type: float

    def __init__(self, data):
        Device.__init__(self, data)
        self.freq = float(self.data)
        self.freq = float(self.data)


class DoorSensor(Device):
    name = "door_sensor"
    description = "Датчик двери"
    id = 106


class PassiveInfraredSensor(Device):
    name = "passive_infrared_sensor"
    description = "PIR датчик (passive infrared)"
    id = 107
    state = None  # type: int
    is_triggered = None  # type: bool
    is_ping = None  # type: bool

    def __init__(self, data):
        Device.__init__(self, data)
        self.state = int(self.data)
        if self.state < 0 or self.state > 1:
            raise ValueError("Wrong order button state value {}".format(state))
        self.is_ping = bool(self.state)
        self.is_triggered = not self.is_triggered


class Seal(Device):
    name = "seal"
    description = "Электронная пломба"
    id = 108
    state = None  # type: int
    is_triggered = None  # type: bool
    is_ping = None  # type: bool

    def __init__(self, data):
        Device.__init__(self, data)
        self.state = int(self.data)
        if self.state < 0 or self.state > 1:
            raise ValueError("Wrong order button state value {}".format(state))
        self.is_triggered = bool(self.state)
        self.is_ping = not self.is_triggered


class Tracker(Device):
    name = "tracker"
    description = "Трекер"
    id = 109
    state = None  # type: int
    is_alert = None  # type: bool
    is_position = None  # type: bool
    lon = None  # type: str
    lat = None  # type: str

    def __init__(self, data):
        Device.__init__(self, data)
        self.state = int(self.data)
        if self.state < 0 or self.state > 1:
            raise ValueError("Wrong order button state value {}".format(state))
        self.is_position = bool(self.state)
        self.is_alert = not self.is_position
        if self.is_position:
            pos_data = self.data_ext
            (self.lon, self.lat) = (s.strip() for s in pos_data.split(","))


class Pinger(Device):
    name = "pinger"
    description = "Тестер сети"
    id = 110


DEVICES_BY_ID = {d.id: d for d in globals().values()
                 if isinstance(d, type) and issubclass(d, Device)}
