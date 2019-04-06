import datetime
import struct
from typing import List, Any

from .Config import Config
from .Exceptions import WrongLength


class MessageData(object):
    """
    Base class for the data section of a message, including some unit conversion methods
    """

    MESSAGETYPE = None

    raw_data: bytearray

    config: Config

    def __init__(self, buffer: bytearray, config: Config):
        self.raw_data = buffer
        self.config = config

    def c_to_f(self, c):
        return (c * 9 / 5) + 32

    def kph_to_knots(self, k):
        return k / 1.852 / 10

    def liters_to_gallons(self, liters):
        return liters / 3.785 / 100

    def millibars_to_hg(self, m):
        """
        convert millibars to inches of mercury
        :param m:
        :return:
        """
        return m / 33.864 / 10

    def millibars_to_psi(self, m):
        return m / 68.948

    def __str__(self):
        return 'data={data!s}...'.format(data=self.raw_data[:10])


class PrimaryFlight(MessageData):
    MESSAGETYPE = 1

    pAltitude: Any
    bAltitude: int
    asi: int
    tas: int
    aoa: int
    vsi: int
    baro: int
    local: int
    oat: int
    humidity: int
    systemFlags: int
    hour: int
    minute: int
    second: int
    date: int
    month: int
    year: int
    ftHour: int
    ftMin: int
    densityAltitude: int

    date_time: datetime

    exception: Exception

    def __init__(self, buffer: bytearray, config: Config):
        super().__init__(buffer, config)

        buffer_len = len(buffer)
        if 32 < buffer_len:
            raise WrongLength(buffer_len, 32)

        (self.pAltitude, self.bAltitude,  # ii
         self.asi, self.tas,  # HH
         self.aoa, self.vsi,  # hh
         self.baro, self.local,  # HH
         self.oat, self.humidity,  # hb
         self.systemFlags,  # B
         self.hour, self.minute, self.second, self.date, self.month, self.year,  # bbbbbb
         self.ftHour, self.ftMin,  # bb
         ) = struct.unpack('ii HH hh HH hb B bbbbbb bb', buffer)

        self._calculate_density_altitude()

        if 'knots' == self.config.units['airspeed']:
            self.asi = self.kph_to_knots(self.asi)
            self.tas = self.kph_to_knots(self.tas)
        self.aoa /= 10
        if 'hg' == self.config.units['barometer']:
            self.baro = self.millibars_to_hg(self.baro)
            self.local = self.millibars_to_hg(self.local)
        if 'f' == self.config.units['ambientTemperature']:
            self.oat = self.c_to_f(self.oat)
        try:
            self.date_time = datetime.datetime(self.year + 2000, self.month, self.date, self.hour, self.minute,
                                               self.second)
        except ValueError as e:
            self.date_time = None
            self.exception = e

    def _calculate_density_altitude(self):
        """
        density altitude calculation from:
        from https://www.flyingmag.com/technique/tip-week/calculating-density-altitude-pencil
        """
        ias_temp = ((self.pAltitude / 1000) * 2 - 15) * -1
        self.densityAltitude = self.pAltitude + (120 * (self.oat - ias_temp))

    def __str__(self):
        return 'PrimaryFlight altitude={alt:.0f} ASI={asi:.0f} VSI={vsi:.0f}'.format(
            alt=self.pAltitude, asi=self.asi, vsi=self.vsi
        )


class GPS(MessageData):
    MESSAGETYPE = 2

    latitude: int
    longitude: int
    gpsAltitude: int
    agl: int
    northVelocity: int
    eastVelocity: int
    downVelocity: int
    groundSpeed: int
    trueTrack: int
    variation: int
    gps: int
    satsTracked: int
    satsVisible: int
    horizontalAccuracy: int
    verticalAccuracy: int
    gpsCapability: int
    raimStatus: int
    raimHError: int
    raimVError: int

    latitudeDegrees: float
    longitudeDegrees: float

    def __init__(self, buffer: bytearray, config: Config):
        super().__init__(buffer, config)
        (self.latitude, self.longitude,  # ii
         self.gpsAltitude, self.agl,  # ii
         self.northVelocity, self.eastVelocity, self.downVelocity,  # iii
         self.groundSpeed, self.trueTrack, self.variation,  # HHh
         self.gps, self.satsTracked, self.satsVisible,  # bbb
         self.horizontalAccuracy, self.verticalAccuracy, self.gpsCapability,  # bbb
         self.raimStatus, self.raimHError, self.raimVError,  # bbb
         ) = struct.unpack_from('ii ii iii HHh bbb bbb bbb x', buffer)

        self.latitude /= 180 / 1000
        self.longitude /= 180 / 1000
        if 'knots' == self.config.units['airspeed']:
            self.groundSpeed = self.kph_to_knots(self.groundSpeed)
        self.trueTrack /= 10

    def __str__(self):
        return 'GPS lat={lat:.4f} lon={lon:.4f} speed={speed:.0f} alt={alt:.0f} agl={agl:.0f}'.format(
            lat=self.latitudeDegrees, lon=self.longitudeDegrees, speed=self.groundSpeed,
            alt=self.gpsAltitude, agl=self.agl
        )


class Attitude(MessageData):
    MESSAGETYPE = 3

    headingMag: int
    pitchAngle: int
    bankAngle: int
    yawAngle: int
    turnRate: int
    slip: int
    gForce: int
    lrForce: int
    frForce: int
    bankRate: int
    pitchRate: int
    yawRate: int
    sensorFlags: int

    def __init__(self, buffer: bytearray, config: Config):
        super().__init__(buffer, config)
        (self.headingMag,  # H
         self.pitchAngle, self.bankAngle, self.yawAngle,  # hhh
         self.turnRate, self.slip,  # hh
         self.gForce, self.lrForce, self.frForce,  # hhh
         self.bankRate, self.pitchRate, self.yawRate,  # hhh
         self.sensorFlags,  # b
         ) = struct.unpack_from('H hhh hh hhh hhh b xxx', buffer)

        self.headingMag /= 10
        self.pitchAngle /= 10
        self.bankAngle /= 10
        self.yawAngle /= 10

    def __str__(self):
        return 'Attitude heading={heading:.0f} pitch={pitch:.1f} bank={bank:.1f}'.format(
            heading=self.headingMag, pitch=self.pitchAngle, bank=self.bankAngle
        )


class EngineData(MessageData):
    """
    engine data with TC inputs hardcoded for N2468Z
    """

    MESSAGETYPE = 10

    engineNumber: int
    engineType: int

    numberOfEgt: int
    numberOfCht: int
    rpm: int
    pulse: int
    oilPressure1: int
    oilPressure2: int
    fuelPressure: int
    coolantTemperature: int
    oilTemperature1: int
    oilTemperature2: int
    auxTemperature1: int
    auxTemperature2: int
    auxTemperature3: int
    auxTemperature4: int
    fuelFlow: int
    auxFlow: int
    manifoldPressure: int
    boostPressure: int
    inletTemperature: int
    ambientPressure: int
    egt: List[float]
    cht: List[float]

    def __init__(self, buffer: bytearray, config: Config):
        super().__init__(buffer, config)
        format_string = 'bb bb HH HHH h hh hhhh HH HH hH '  # 40 bytes
        (self.engineNumber, self.engineType,  # bb
         self.numberOfEgt, self.numberOfCht,  # bb
         self.rpm, self.pulse,  # HH
         self.oilPressure1, self.oilPressure2, self.fuelPressure,  # HHH
         self.coolantTemperature,  # h
         self.oilTemperature1, self.oilTemperature2,  # hh
         self.auxTemperature1, self.auxTemperature2, self.auxTemperature3, self.auxTemperature4,  # hhhh
         self.fuelFlow, self.auxFlow,  # HH
         self.manifoldPressure, self.boostPressure,  # HH
         self.inletTemperature, self.ambientPressure,  # hH
         ) = struct.unpack_from(format_string, buffer)

        self._unpack_thermocouples(buffer)

        self._convert_units()

    def _unpack_thermocouples(self, buffer):
        """
        the RDAC has 12 themocouple inputs but no info on how each is used gets included in the messages.
        unpack them into arrays of CHT and EGT values.
        ignore any messages that have an incomplete set of values because we don't know how to parse partial values
        :param buffer:
        :return:
        """
        qty_assigned_thermocouples = 0
        for v in self.config.thermocouples.values():
            if v is not None:
                qty_assigned_thermocouples += 1

        self.cht = []
        self.egt = []
        if qty_assigned_thermocouples == (self.numberOfCht + self.numberOfEgt):
            format_string = 'h' * self.numberOfEgt + 'h' * self.numberOfCht
            egt_cht_temp = struct.unpack_from(format_string, buffer, 40)

            for i in range(0, qty_assigned_thermocouples):
                if 'cht' == self.config.thermocouples[i + 1]:
                    self.cht.append(egt_cht_temp[i])
                elif 'egt' == self.config.thermocouples[i + 1]:
                    self.egt.append(egt_cht_temp[i])

    def _convert_units(self):
        if 'f' == self.config.units['engineTemperature']:
            self.coolantTemperature = self.c_to_f(self.coolantTemperature)
            self.oilTemperature1 = self.c_to_f(self.oilTemperature1)
            self.oilTemperature2 = self.c_to_f(self.oilTemperature2)

            self.auxTemperature1 = self.c_to_f(self.auxTemperature1)
            self.auxTemperature2 = self.c_to_f(self.auxTemperature2)
            self.auxTemperature3 = self.c_to_f(self.auxTemperature3)
            self.auxTemperature4 = self.c_to_f(self.auxTemperature4)

            self.inletTemperature = self.c_to_f(self.inletTemperature)

            for i in range(0, len(self.egt)):
                self.egt[i] = self.c_to_f(self.egt[i])
            for i in range(0, len(self.cht)):
                self.cht[i] = self.c_to_f(self.cht[i])

        if 'hg' == self.config.units['barometer']:
            self.ambientPressure = self.millibars_to_hg(self.ambientPressure)

        if 'hg' == self.config.units['manifoldPressure']:
            self.manifoldPressure = self.millibars_to_hg(self.manifoldPressure)

        if 'psi' == self.config.units['oilPressure']:
            self.oilPressure1 = self.millibars_to_psi(self.oilPressure1)
            self.oilPressure2 = self.millibars_to_psi(self.oilPressure2)

        if 'gallons' == self.config.units['fuel']:
            self.fuelFlow = self.liters_to_gallons(self.fuelFlow)

    def __str__(self):
        return 'EngineData RPM={rpm} OilP={oilp:.0f} OilT={oilt:.0f} MAP={map:.2f} FuelF={fuelf:.1f} EGT={egt!s} CHT={cht!s}'.format(
            rpm=self.rpm, oilp=self.oilPressure1, oilt=self.oilTemperature1,
            map=self.manifoldPressure, fuelf=self.fuelFlow, egt=self.egt, cht=self.cht
        )
