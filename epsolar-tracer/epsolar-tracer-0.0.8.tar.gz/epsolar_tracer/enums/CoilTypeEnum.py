import enum


@enum.unique
class CoilTypeEnum(enum.IntEnum):
    # Manual control the load
    MANUAL_CONTROL_THE_LOAD = 1

    # Enable load test mode
    ENABLE_LOAD_TEST_MODE = 2

    # Force the load on/off
    FORCE_THE_LOAD_ON_OFF = 3

    # Over temperature inside the device
    OVER_TEMPERATURE_INSIDE_THE_DEVICE = 4

    # Day/Night
    DAY_NIGHT = 5
