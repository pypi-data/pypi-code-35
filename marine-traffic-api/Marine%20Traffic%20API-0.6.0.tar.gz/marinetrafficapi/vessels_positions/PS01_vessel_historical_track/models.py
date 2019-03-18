from marinetrafficapi.models import Model
from marinetrafficapi.fields import NumberField, RealNumberField, DatetimeField


class VesselHistoricalPosition(Model):
    """Get all vessel historical positions for a specific period of time."""

    mmsi = NumberField(index='MMSI',
                       desc="Maritime Mobile Service Identity - a nine-digit number "
                            "sent in digital form over a radio frequency that identifies "
                            "the vessel's transmitter station")

    status = NumberField(index='STATUS',
                         desc="The AIS Navigational Status of the subject vessel as "
                              "input by the vessel's crew - more. There might be "
                              "discrepancies with the vessel's detail page when vessel "
                              "speed is near zero (0) knots.")

    speed = NumberField(index='SPEED',
                        desc="The speed (in knots x10) that the subject vessel is "
                             "reporting according to AIS transmissions")

    longitude = RealNumberField(index='LON',
                                desc="A geographic coordinate that specifies the "
                                     "east-west position of the vessel on the "
                                     "Earth's surface")

    latitude = RealNumberField(index='LAT',
                               desc="a geographic coordinate that specifies the "
                                    "north-south position of the vessel on the "
                                    "Earth's surface")

    course = NumberField(index='COURSE',
                         desc="The course (in degrees) that the subject vessel is "
                              "reporting according to AIS transmissions")

    heading = NumberField(index='HEADING',
                          desc="The heading (in degrees) that the subject vessel is "
                               "reporting according to AIS transmissions")

    timestamp = DatetimeField(index='TIMESTAMP',
                              desc="The date and time (in UTC) that the subject vessel's "
                                   "position was recorded by MarineTraffic",
                              format='%Y-%m-%dT%H:%M:%S')

    ship_id = NumberField(index='SHIP_ID',
                          desc="A uniquely assigned ID by MarineTraffic "
                               "for the subject vessel")

    wind_angle = NumberField(index='WIND_ANGLE',
                             desc="The current angle of the wind in the subject area "
                                  "(in degrees, compared to True North)")

    wind_speed = NumberField(index='WIND_SPEED',
                             desc="The current wind speed in the subject area (in knots)")

    wind_temp = NumberField(index='WIND_TEMP',
                            desc="The current temperature of the wind in the "
                                 "subject area (in Celsius degrees)")
