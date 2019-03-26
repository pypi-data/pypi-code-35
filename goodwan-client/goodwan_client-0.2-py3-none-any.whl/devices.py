"""
GoodWan client library: devices
"""
from goodwan_client.classes import Basic


class Device(Basic):
    name = "unknown"
    description = "unknown"
    id = -1
    is_ping = False   # type: bool

    def __init__(self, data):
        self.data = data["data"]
        self.data_ext = data["data_ext"]

    def state_desc(self):
        """ State description (str) """
        raise NotImplementedError("State description not implemented")


class TempSensor(Device):
    name = "temp_sensor"
    description = "Датчик температуры"
    id = 101
    temp = None  # type: float

    def __init__(self, data):
        Device.__init__(self, data)
        self.temp = float(self.data)

    def state_desc(self):
        return "temperature: {}".format(self.temp)


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
            raise ValueError("Wrong order button state value {}"
                             .format(self.state))
        self.is_cancel = bool(self.state)
        self.is_order = not self.is_cancel

    def state_desc(self):
        return "order" if self.is_order else "cancel"


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

    def state_desc(self):
        return "pulse 1: {}, pulse2: {}".format(self.pulse1, self.pulse2)


class LevelSensor(Device):
    name = "level_sensor"
    description = "Датчик уровня"
    id = 104
    level = None  # type: float

    def __init__(self, data):
        Device.__init__(self, data)
        self.level = float(self.data)

    def state_desc(self):
        return "level: {}".format(self.level)


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

    def state_desc(self):
        return "freq: {}, amp: {}".format(self.freq, self.amp)


class DoorSensor(Device):
    name = "door_sensor"
    description = "Датчик двери"
    id = 106

    def state_desc(self):
        return "open"


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
            raise ValueError("Wrong infrared sensor state value {}"
                             .format(self.state))
        self.is_ping = bool(self.state)
        self.is_triggered = not self.is_triggered

    def state_desc(self):
        return "triggered" if self.is_triggered else "ping"


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
            raise ValueError("Wrong order seal state value {}"
                             .format(self.state))
        self.is_triggered = bool(self.state)
        self.is_ping = not self.is_triggered

    def state_desc(self):
        return "triggered" if self.is_triggered else "ping"


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
            raise ValueError("Wrong tracker state value {}"
                             .format(self.state))
        self.is_position = bool(self.state)
        self.is_alert = not self.is_position
        if self.is_position:
            pos_data = self.data_ext
            (self.lon, self.lat) = (s.strip() for s in pos_data.split(","))

    def state_desc(self):
        if self.is_position:
            return "position: lat {} lon {}".format(self.lat, self.lon)
        else:
            return "alert"


class Pinger(Device):
    name = "pinger"
    description = "Тестер сети"
    id = 110
    is_ping = True

    def state_desc(self):
        return "ping"


DEVICES_BY_ID = {d.id: d for d in globals().values()
                 if isinstance(d, type) and issubclass(d, Device)}
