import enum


@enum.unique
class RegisterTypeEnum(enum.IntEnum):
    # Charging equipment rated input voltage
    CHARGING_EQUIPMENT_RATED_INPUT_VOLTAGE = 1

    # Charging equipment rated input current
    CHARGING_EQUIPMENT_RATED_INPUT_CURRENT = 2

    # Charging equipment rated input power
    CHARGING_EQUIPMENT_RATED_INPUT_POWER = 3

    # Charging equipment rated input power L
    CHARGING_EQUIPMENT_RATED_INPUT_POWER_L = 4

    # Charging equipment rated input power H
    CHARGING_EQUIPMENT_RATED_INPUT_POWER_H = 5

    # Charging equipment rated output voltage
    CHARGING_EQUIPMENT_RATED_OUTPUT_VOLTAGE = 6

    # Charging equipment rated output current
    CHARGING_EQUIPMENT_RATED_OUTPUT_CURRENT = 7

    # Charging equipment rated output power
    CHARGING_EQUIPMENT_RATED_OUTPUT_POWER = 8

    # Charging equipment rated output power L
    CHARGING_EQUIPMENT_RATED_OUTPUT_POWER_L = 9

    # Charging equipment rated output power H
    CHARGING_EQUIPMENT_RATED_OUTPUT_POWER_H = 10

    # Charging mode
    CHARGING_MODE = 11

    # Rated output current of load
    RATED_OUTPUT_CURRENT_OF_LOAD = 12

    # Charging equipment input voltage
    CHARGING_EQUIPMENT_INPUT_VOLTAGE = 13

    # Charging equipment input current
    CHARGING_EQUIPMENT_INPUT_CURRENT = 14

    # Charging equipment input power
    CHARGING_EQUIPMENT_INPUT_POWER = 15

    # Charging equipment input power L
    CHARGING_EQUIPMENT_INPUT_POWER_L = 16

    # Charging equipment input power H
    CHARGING_EQUIPMENT_INPUT_POWER_H = 17

    # Charging equipment output voltage
    CHARGING_EQUIPMENT_OUTPUT_VOLTAGE = 18

    # Charging equipment output current
    CHARGING_EQUIPMENT_OUTPUT_CURRENT = 19

    # Charging equipment output power
    CHARGING_EQUIPMENT_OUTPUT_POWER = 20

    # Charging equipment output power L
    CHARGING_EQUIPMENT_OUTPUT_POWER_L = 21

    # Charging equipment output power H
    CHARGING_EQUIPMENT_OUTPUT_POWER_H = 22

    # Discharging equipment output voltage
    DISCHARGING_EQUIPMENT_OUTPUT_VOLTAGE = 23

    # Discharging equipment output current
    DISCHARGING_EQUIPMENT_OUTPUT_CURRENT = 24

    # Discharging equipment output power
    DISCHARGING_EQUIPMENT_OUTPUT_POWER = 25

    # Discharging equipment output power L
    DISCHARGING_EQUIPMENT_OUTPUT_POWER_L = 26

    # Discharging equipment output power H
    DISCHARGING_EQUIPMENT_OUTPUT_POWER_H = 27

    # Battery Temperature
    BATTERY_TEMPERATURE = 28

    # Temperature inside equipment
    TEMPERATURE_INSIDE_EQUIPMENT = 29

    # Power components temperature
    POWER_COMPONENTS_TEMPERATURE = 30

    # Battery SOC
    BATTERY_SOC = 31

    # Remote battery temperature
    REMOTE_BATTERY_TEMPERATURE = 32

    # Battery's real rated power
    BATTERYS_REAL_RATED_POWER = 33

    # Battery status
    BATTERY_STATUS = 34

    # Charging equipment status
    CHARGING_EQUIPMENT_STATUS = 35

    # Maximum input volt (PV) today
    MAXIMUM_INPUT_VOLT_PV_TODAY = 36

    # Minimum input volt (PV) today
    MINIMUM_INPUT_VOLT_PV_TODAY = 37

    # Maximum battery volt today
    MAXIMUM_BATTERY_VOLT_TODAY = 38

    # Minimum battery volt today
    MINIMUM_BATTERY_VOLT_TODAY = 39

    # Consumed energy today
    CONSUMED_ENERGY_TODAY = 40

    # Consumed energy today L
    CONSUMED_ENERGY_TODAY_L = 41

    # Consumed energy today H
    CONSUMED_ENERGY_TODAY_H = 42

    # Consumed energy this month
    CONSUMED_ENERGY_THIS_MONTH = 43

    # Consumed energy this month L
    CONSUMED_ENERGY_THIS_MONTH_L = 44

    # Consumed energy this month H
    CONSUMED_ENERGY_THIS_MONTH_H = 45

    # Consumed energy this year
    CONSUMED_ENERGY_THIS_YEAR = 46

    # Consumed energy this year L
    CONSUMED_ENERGY_THIS_YEAR_L = 47

    # Consumed energy this year H
    CONSUMED_ENERGY_THIS_YEAR_H = 48

    # Total consumed energy
    TOTAL_CONSUMED_ENERGY = 49

    # Total consumed energy L
    TOTAL_CONSUMED_ENERGY_L = 50

    # Total consumed energy H
    TOTAL_CONSUMED_ENERGY_H = 51

    # Generated energy today
    GENERATED_ENERGY_TODAY = 52

    # Generated energy today L
    GENERATED_ENERGY_TODAY_L = 53

    # Generated energy today H
    GENERATED_ENERGY_TODAY_H = 54

    # Generated energy this month
    GENERATED_ENERGY_THIS_MONTH = 55

    # Generated energy this month L
    GENERATED_ENERGY_THIS_MONTH_L = 56

    # Generated energy this month H
    GENERATED_ENERGY_THIS_MONTH_H = 57

    # Generated energy this year
    GENERATED_ENERGY_THIS_YEAR = 58

    # Generated energy this year L
    GENERATED_ENERGY_THIS_YEAR_L = 59

    # Generated energy this year H
    GENERATED_ENERGY_THIS_YEAR_H = 60

    # Total generated energy
    TOTAL_GENERATED_ENERGY = 61

    # Total generated energy L
    TOTAL_GENERATED_ENERGY_L = 62

    # Total Generated energy H
    TOTAL_GENERATED_ENERGY_H = 63

    # Carbon dioxide reduction
    CARBON_DIOXIDE_REDUCTION = 64

    # Carbon dioxide reduction L
    CARBON_DIOXIDE_REDUCTION_L = 65

    # Carbon dioxide reduction H
    CARBON_DIOXIDE_REDUCTION_H = 66

    # Battery Current
    BATTERY_CURRENT = 67

    # Battery Current L
    BATTERY_CURRENT_L = 68

    # Battery Current H
    BATTERY_CURRENT_H = 69

    # Battery Temp.
    BATTERY_TEMP = 70

    # Ambient Temp.
    AMBIENT_TEMP = 71

    # Battery Type
    BATTERY_TYPE = 72

    # Battery Capacity
    BATTERY_CAPACITY = 73

    # Temperature compensation coefficient
    TEMPERATURE_COMPENSATION_COEFFICIENT = 74

    # High Volt.disconnect
    HIGH_VOLT_DISCONNECT = 75

    # Charging limit voltage
    CHARGING_LIMIT_VOLTAGE = 76

    # Over voltage reconnect
    OVER_VOLTAGE_RECONNECT = 77

    # Equalization voltage
    EQUALIZATION_VOLTAGE = 78

    # Boost voltage
    BOOST_VOLTAGE = 79

    # Float voltage
    FLOAT_VOLTAGE = 80

    # Boost reconnect voltage
    BOOST_RECONNECT_VOLTAGE = 81

    # Low voltage reconnect
    LOW_VOLTAGE_RECONNECT = 82

    # Under voltage recover
    UNDER_VOLTAGE_RECOVER = 83

    # Under voltage warning
    UNDER_VOLTAGE_WARNING = 84

    # Low voltage disconnect
    LOW_VOLTAGE_DISCONNECT = 85

    # Discharging limit voltage
    DISCHARGING_LIMIT_VOLTAGE = 86

    # Real time clock 1
    REAL_TIME_CLOCK_1 = 87

    # Real time clock 2
    REAL_TIME_CLOCK_2 = 88

    # Real time clock 3
    REAL_TIME_CLOCK_3 = 89

    # Equalization charging cycle
    EQUALIZATION_CHARGING_CYCLE = 90

    # Battery temperature warning upper limit
    BATTERY_TEMPERATURE_WARNING_UPPER_LIMIT = 91

    # Battery temperature warning lower limit
    BATTERY_TEMPERATURE_WARNING_LOWER_LIMIT = 92

    # Controller inner temperature upper limit
    CONTROLLER_INNER_TEMPERATURE_UPPER_LIMIT = 93

    # Controller inner temperature upper limit recover
    CONTROLLER_INNER_TEMPERATURE_UPPER_LIMIT_RECOVER = 94

    # Power component temperature upper limit
    POWER_COMPONENT_TEMPERATURE_UPPER_LIMIT = 95

    # Power component temperature upper limit recover
    POWER_COMPONENT_TEMPERATURE_UPPER_LIMIT_RECOVER = 96

    # Line Impedance
    LINE_IMPEDANCE = 97

    # Night TimeThreshold Volt.(NTTV)
    NIGHT_TIMETHRESHOLD_VOLT_NTTV = 98

    # Light signal startup (night) delay time
    LIGHT_SIGNAL_STARTUP_NIGHT_DELAY_TIME = 99

    # Day Time Threshold Volt.(DTTV)
    DAY_TIME_THRESHOLD_VOLT_DTTV = 100

    # Light signal turn off(day) delay time
    LIGHT_SIGNAL_TURN_OFF_DAY_DELAY_TIME = 101

    # Load controling modes
    LOAD_CONTROLING_MODES = 102

    # Working time length 1
    WORKING_TIME_LENGTH_1 = 103

    # Working time length 2
    WORKING_TIME_LENGTH_2 = 104

    # Turn on timing 1 sec
    TURN_ON_TIMING_1_SEC = 105

    # Turn on timing 1 min
    TURN_ON_TIMING_1_MIN = 106

    # Turn on timing 1 hour
    TURN_ON_TIMING_1_HOUR = 107

    # Turn off timing 1 sec
    TURN_OFF_TIMING_1_SEC = 108

    # Turn off timing 1 min
    TURN_OFF_TIMING_1_MIN = 109

    # Turn off timing 1 hour
    TURN_OFF_TIMING_1_HOUR = 110

    # Turn on timing 2 sec
    TURN_ON_TIMING_2_SEC = 111

    # Turn on timing 2 min
    TURN_ON_TIMING_2_MIN = 112

    # Turn on timing 2 hour
    TURN_ON_TIMING_2_HOUR = 113

    # Turn off timing 2 sec
    TURN_OFF_TIMING_2_SEC = 114

    # Turn off timing 2 min
    TURN_OFF_TIMING_2_MIN = 115

    # Turn off timing 2 hour
    TURN_OFF_TIMING_2_HOUR = 116

    # Length of night
    LENGTH_OF_NIGHT = 117

    # Battery rated voltage code
    BATTERY_RATED_VOLTAGE_CODE = 118

    # Load timing control selection
    LOAD_TIMING_CONTROL_SELECTION = 119

    # Default Load On/Off in manual mode
    DEFAULT_LOAD_ON_OFF_IN_MANUAL_MODE = 120

    # Equalize duration
    EQUALIZE_DURATION = 121

    # Boost duration
    BOOST_DURATION = 122

    # Discharging percentage
    DISCHARGING_PERCENTAGE = 123

    # Charging percentage
    CHARGING_PERCENTAGE = 124

    # Management modes of battery charging and discharging
    MANAGEMENT_MODES_OF_BATTERY_CHARGING_AND_DISCHARGING = 125
