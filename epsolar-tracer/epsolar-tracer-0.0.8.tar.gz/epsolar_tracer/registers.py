# -*- coding: iso-8859-15 -*-
#
# From the PDF

# ---------------------------------------------------------------------------#
# Logging
# ---------------------------------------------------------------------------#
import logging

from epsolar_tracer.Register import Register
from epsolar_tracer.Coil import Coil
from epsolar_tracer.units import V, A, W, I, C, PC, KWH, Ton, AH, MO, MIN, SEC, HOUR
from epsolar_tracer.enums.RegisterTypeEnum import RegisterTypeEnum
from epsolar_tracer.enums.CoilTypeEnum import CoilTypeEnum

_logger = logging.getLogger(__name__)


# LS-B Series Protocol
# ModBus Register Address List
# Beijing Epsolar Technology Co., Ltd.
# Notes :
# (1)The ID of the controller is 1 by default and can be modified by PC software(Solar Station Monitor) or
# remote meter MT50.
# (2)The serial communication parameters: 115200bps baudrate, 8 data bits, 1 stop bit and no parity,no
# handshaking.
# (3)The register address below is in hexadecimal format.
# (4)For the data with the length of 32 bits, such as power, using the L and H registers represent the low and
# high 16 bits value,respectively. e.g.The charging input rated power is actually 3000W, multiples of 100 times,
# then the value of 0x3002 register is 0x93E0 and value of 0x3003 is 0x0004

# V1.1
# Variable name, Address, Description, Unit, Times

# Rated data (read only) input register
registers = {
    # Charging equipment rated input voltage
    RegisterTypeEnum.CHARGING_EQUIPMENT_RATED_INPUT_VOLTAGE: Register("Charging equipment rated input voltage", 0x3000, "PV array rated voltage", V, 100),
    # Charging equipment rated input current
    RegisterTypeEnum.CHARGING_EQUIPMENT_RATED_INPUT_CURRENT: Register("Charging equipment rated input current", 0x3001, "PV array rated current", A, 100),
    # Charging equipment rated input power
    RegisterTypeEnum.CHARGING_EQUIPMENT_RATED_INPUT_POWER: Register("Charging equipment rated input power", 0x3002, "PV array rated power", W, 100, 2),
    # Charging equipment rated input power L
    RegisterTypeEnum.CHARGING_EQUIPMENT_RATED_INPUT_POWER_L: Register("Charging equipment rated input power L", 0x3002, "PV array rated power (low 16 bits)", W, 100),
    # Charging equipment rated input power H
    RegisterTypeEnum.CHARGING_EQUIPMENT_RATED_INPUT_POWER_H: Register("Charging equipment rated input power H", 0x3003, "PV array rated power (high 16 bits)", W, 100),
    # Charging equipment rated output voltage
    RegisterTypeEnum.CHARGING_EQUIPMENT_RATED_OUTPUT_VOLTAGE: Register("Charging equipment rated output voltage", 0x3004, "Battery's voltage", V, 100),
    # Charging equipment rated output current
    RegisterTypeEnum.CHARGING_EQUIPMENT_RATED_OUTPUT_CURRENT: Register("Charging equipment rated output current", 0x3005, "Rated charging current to battery", A, 100),
    # Charging equipment rated output power
    RegisterTypeEnum.CHARGING_EQUIPMENT_RATED_OUTPUT_POWER: Register("Charging equipment rated output power", 0x3006, "Rated charging power to battery", W, 100, 2),
    # Charging equipment rated output power L
    RegisterTypeEnum.CHARGING_EQUIPMENT_RATED_OUTPUT_POWER_L: Register("Charging equipment rated output power L", 0x3006, "Rated charging power to battery H", W, 100),
    # Charging equipment rated output power H
    RegisterTypeEnum.CHARGING_EQUIPMENT_RATED_OUTPUT_POWER_H: Register("Charging equipment rated output power H", 0x3007, "Charging equipment rated output power H", W, 100),
    # Charging mode
    RegisterTypeEnum.CHARGING_MODE: Register("Charging mode", 0x3008, "0001H-PWM", I, 1),
    # Rated output current of load
    RegisterTypeEnum.RATED_OUTPUT_CURRENT_OF_LOAD: Register("Rated output current of load", 0x300E, "Rated output current of load", A, 100),

    # Real-time data (read only) input register
    # Charging equipment input voltage
    RegisterTypeEnum.CHARGING_EQUIPMENT_INPUT_VOLTAGE: Register("Charging equipment input voltage", 0x3100, "Solar charge controller--PV array voltage", V, 100),
    # Charging equipment input current
    RegisterTypeEnum.CHARGING_EQUIPMENT_INPUT_CURRENT: Register("Charging equipment input current", 0x3101, "Solar charge controller--PV array current", A, 100),
    # Charging equipment input power
    RegisterTypeEnum.CHARGING_EQUIPMENT_INPUT_POWER: Register("Charging equipment input power", 0x3102, "Solar charge controller--PV array power", W, 100, 2),
    # Charging equipment input power L
    RegisterTypeEnum.CHARGING_EQUIPMENT_INPUT_POWER_L: Register("Charging equipment input power L", 0x3102, "Solar charge controller--PV array power", W, 100),
    # Charging equipment input power H
    RegisterTypeEnum.CHARGING_EQUIPMENT_INPUT_POWER_H: Register("Charging equipment input power H", 0x3103, "Charging equipment input power H", W, 100),
    # Charging equipment output voltage
    RegisterTypeEnum.CHARGING_EQUIPMENT_OUTPUT_VOLTAGE: Register("Charging equipment output voltage", 0x3104, "Battery voltage", V, 100),
    # Charging equipment output current
    RegisterTypeEnum.CHARGING_EQUIPMENT_OUTPUT_CURRENT: Register("Charging equipment output current", 0x3105, "Battery charging current", A, 100),
    # Charging equipment output power
    RegisterTypeEnum.CHARGING_EQUIPMENT_OUTPUT_POWER: Register("Charging equipment output power", 0x3106, "Battery charging power", W, 100, 2),
    # Charging equipment output power L
    RegisterTypeEnum.CHARGING_EQUIPMENT_OUTPUT_POWER_L: Register("Charging equipment output power L", 0x3106, "Battery charging power", W, 100),
    # Charging equipment output power H
    RegisterTypeEnum.CHARGING_EQUIPMENT_OUTPUT_POWER_H: Register("Charging equipment output power H", 0x3107, "Charging equipment output power H", W, 100),
    # Discharging equipment output voltage
    RegisterTypeEnum.DISCHARGING_EQUIPMENT_OUTPUT_VOLTAGE: Register("Discharging equipment output voltage", 0x310C, "Load voltage", V, 100),
    # Discharging equipment output current
    RegisterTypeEnum.DISCHARGING_EQUIPMENT_OUTPUT_CURRENT: Register("Discharging equipment output current", 0x310D, "Load current", A, 100),
    # Discharging equipment output power
    RegisterTypeEnum.DISCHARGING_EQUIPMENT_OUTPUT_POWER: Register("Discharging equipment output power", 0x310E, "Load power", W, 100, 2),
    # Discharging equipment output power L
    RegisterTypeEnum.DISCHARGING_EQUIPMENT_OUTPUT_POWER_L: Register("Discharging equipment output power L", 0x310E, "Load power L", W, 100),
    # Discharging equipment output power H
    RegisterTypeEnum.DISCHARGING_EQUIPMENT_OUTPUT_POWER_H: Register("Discharging equipment output power H", 0x310F, "Discharging equipment output power H", W, 100),
    # Battery Temperature
    RegisterTypeEnum.BATTERY_TEMPERATURE: Register("Battery Temperature", 0x3110, "Battery Temperature", C, 100),
    # Temperature inside equipment
    RegisterTypeEnum.TEMPERATURE_INSIDE_EQUIPMENT: Register("Temperature inside equipment", 0x3111, "Temperature inside case", C, 100),
    # Power components temperature
    RegisterTypeEnum.POWER_COMPONENTS_TEMPERATURE: Register("Power components temperature", 0x3112, "Heat sink surface temperature of equipments' power components", C, 100),
    # Battery SOC
    RegisterTypeEnum.BATTERY_SOC: Register("Battery SOC", 0x311A, "The percentage of battery's remaining capacity", PC, 1),
    # Remote battery temperature
    RegisterTypeEnum.REMOTE_BATTERY_TEMPERATURE: Register("Remote battery temperature", 0x311B, "The battery tempeture measured by remote temperature sensor", C, 100),
    # Battery's real rated power
    RegisterTypeEnum.BATTERYS_REAL_RATED_POWER: Register("Battery's real rated power", 0x311D, "Current system rated votlage. 1200, 2400 represent 12V, 24V", V, 100),

    # Real-time status (read-only) input re
    # Battery statusgister
    RegisterTypeEnum.BATTERY_STATUS: Register("Battery status", 0x3200, "D3-D0: 01H Overvolt , 00H Normal , 02H Under Volt, 03H Low Volt Disconnect, 04H Fault D7-D4: 00H Normal, 01H Over Temp.(Higher than the warning settings), 02H Low Temp.( Lower than the warning settings), D8: Battery inerternal resistance abnormal 1, normal 0 D15: 1-Wrong identification for rated voltage", I, 1),
    # Charging equipment status
    RegisterTypeEnum.CHARGING_EQUIPMENT_STATUS: Register("Charging equipment status", 0x3201, "D15-D14: Input volt status. 00 normal, 01 no power connected, 02H Higher volt input, 03H Input volt error. D13: Charging MOSFET is short. D12: Charging or Anti-reverse MOSFET is short. D11: Anti-reverse MOSFET is short. D10: Input is over current. D9: The load is Over current. D8: The load is short. D7: Load MOSFET is short. D4: PV Input is short. D3-2: Charging status. 00 No charging,01 Float,02 Boost,03 Equlization. D1: 0 Normal, 1 Fault. D0: 1 Running, 0 Standby.", I, 1),

    # Statistical parameter (read only) input register

    # Maximum input volt (PV) today
    RegisterTypeEnum.MAXIMUM_INPUT_VOLT_PV_TODAY: Register("Maximum input volt (PV) today", 0x3300, "00: 00 Refresh every day", V, 100),
    # Minimum input volt (PV) today
    RegisterTypeEnum.MINIMUM_INPUT_VOLT_PV_TODAY: Register("Minimum input volt (PV) today", 0x3301, "00: 00 Refresh every day", V, 100),
    # Maximum battery volt today
    RegisterTypeEnum.MAXIMUM_BATTERY_VOLT_TODAY: Register("Maximum battery volt today", 0x3302, "00: 00 Refresh every day", V, 100),
    # Minimum battery volt today
    RegisterTypeEnum.MINIMUM_BATTERY_VOLT_TODAY: Register("Minimum battery volt today", 0x3303, "00: 00 Refresh every day", V, 100),
    # Consumed energy today
    RegisterTypeEnum.CONSUMED_ENERGY_TODAY: Register("Consumed energy today", 0x3304, "00: 00 Clear every day", KWH, 100, 2),
    # Consumed energy today L
    RegisterTypeEnum.CONSUMED_ENERGY_TODAY_L: Register("Consumed energy today L", 0x3304, "00: 00 Clear every day", KWH, 100),
    # Consumed energy today H
    RegisterTypeEnum.CONSUMED_ENERGY_TODAY_H: Register("Consumed energy today H", 0x3305, "Consumed energy today H", KWH, 100),
    # Consumed energy this month
    RegisterTypeEnum.CONSUMED_ENERGY_THIS_MONTH: Register("Consumed energy this month", 0x3306, "00: 00 Clear on the first day of month", KWH, 100, 2),
    # Consumed energy this month L
    RegisterTypeEnum.CONSUMED_ENERGY_THIS_MONTH_L: Register("Consumed energy this month L", 0x3306, "00: 00 Clear on the first day of month", KWH, 100),
    # Consumed energy this month H
    RegisterTypeEnum.CONSUMED_ENERGY_THIS_MONTH_H: Register("Consumed energy this month H", 0x3307, "Consumed energy this month H", KWH, 100),
    # Consumed energy this year
    RegisterTypeEnum.CONSUMED_ENERGY_THIS_YEAR: Register("Consumed energy this year", 0x3308, "00: 00 Clear on 1, Jan.", KWH, 100, 2),
    # Consumed energy this year L
    RegisterTypeEnum.CONSUMED_ENERGY_THIS_YEAR_L: Register("Consumed energy this year L", 0x3308, "00: 00 Clear on 1, Jan.", KWH, 100),
    # Consumed energy this year H
    RegisterTypeEnum.CONSUMED_ENERGY_THIS_YEAR_H: Register("Consumed energy this year H", 0x3309, "Consumed energy this year H", KWH, 100),
    # Total consumed energy
    RegisterTypeEnum.TOTAL_CONSUMED_ENERGY: Register("Total consumed energy", 0x330A, "Total consumed energy", KWH, 100, 2),
    # Total consumed energy L
    RegisterTypeEnum.TOTAL_CONSUMED_ENERGY_L: Register("Total consumed energy L", 0x330A, "Total consumed energy L", KWH, 100),
    # Total consumed energy H
    RegisterTypeEnum.TOTAL_CONSUMED_ENERGY_H: Register("Total consumed energy H", 0x330B, "Total consumed energy H", KWH, 100),
    # Generated energy today
    RegisterTypeEnum.GENERATED_ENERGY_TODAY: Register("Generated energy today", 0x330C, "00: 00 Clear every day.", KWH, 100, 2),
    # Generated energy today L
    RegisterTypeEnum.GENERATED_ENERGY_TODAY_L: Register("Generated energy today L", 0x330C, "00: 00 Clear every day.", KWH, 100),
    # Generated energy today H
    RegisterTypeEnum.GENERATED_ENERGY_TODAY_H: Register("Generated energy today H", 0x330D, "Generated energy today H", KWH, 100),
    # Generated energy this month
    RegisterTypeEnum.GENERATED_ENERGY_THIS_MONTH: Register("Generated energy this month", 0x330E, "00: 00 Clear on the first day of month.", KWH, 100, 2),
    # Generated energy this month L
    RegisterTypeEnum.GENERATED_ENERGY_THIS_MONTH_L: Register("Generated energy this month L", 0x330E, "00: 00 Clear on the first day of month.", KWH, 100),
    # Generated energy this month H
    RegisterTypeEnum.GENERATED_ENERGY_THIS_MONTH_H: Register("Generated energy this month H", 0x330F, "Generated energy this month H", KWH, 100),
    # Generated energy this year
    RegisterTypeEnum.GENERATED_ENERGY_THIS_YEAR: Register("Generated energy this year", 0x3310, "00: 00 Clear on 1, Jan.", KWH, 100, 2),
    # Generated energy this year L
    RegisterTypeEnum.GENERATED_ENERGY_THIS_YEAR_L: Register("Generated energy this year L", 0x3310, "00: 00 Clear on 1, Jan.", KWH, 100),
    # Generated energy this year H
    RegisterTypeEnum.GENERATED_ENERGY_THIS_YEAR_H: Register("Generated energy this year H", 0x3311, "Generated energy this year H", KWH, 100),
    # Total generated energy
    RegisterTypeEnum.TOTAL_GENERATED_ENERGY: Register("Total generated energy", 0x3312, "Total generated energy", KWH, 100, 2),
    # Total generated energy L
    RegisterTypeEnum.TOTAL_GENERATED_ENERGY_L: Register("Total generated energy L", 0x3312, "Total generated energy L", KWH, 100),
    # Total Generated energy H
    RegisterTypeEnum.TOTAL_GENERATED_ENERGY_H: Register("Total Generated energy H", 0x3313, "Total Generated energy H", KWH, 100),
    # Carbon dioxide reduction
    RegisterTypeEnum.CARBON_DIOXIDE_REDUCTION: Register("Carbon dioxide reduction", 0x3314, "Saving 1 Kilowatt=Reduction 0.997KG''Carbon dioxide ''=Reduction 0.272KG''Carton''", Ton, 100, 2),
    # Carbon dioxide reduction L
    RegisterTypeEnum.CARBON_DIOXIDE_REDUCTION_L: Register("Carbon dioxide reduction L", 0x3314, "Saving 1 Kilowatt=Reduction 0.997KG''Carbon dioxide ''=Reduction 0.272KG''Carton''", Ton, 100),
    # Carbon dioxide reduction H
    RegisterTypeEnum.CARBON_DIOXIDE_REDUCTION_H: Register("Carbon dioxide reduction H", 0x3315, "Carbon dioxide reduction H", Ton, 100),
    # Battery Current
    RegisterTypeEnum.BATTERY_CURRENT: Register("Battery Current", 0x331B, "The net battery current,charging current minus the discharging one. The positive value represents charging and negative, discharging.", A, 100, 2),
    # Battery Current L
    RegisterTypeEnum.BATTERY_CURRENT_L: Register("Battery Current L", 0x331B, "The net battery current,charging current minus the discharging one. The positive value represents charging and negative, discharging.", A, 100),
    # Battery Current H
    RegisterTypeEnum.BATTERY_CURRENT_H: Register("Battery Current H", 0x331C, "Battery Current H", A, 100),
    # Battery Temp.
    RegisterTypeEnum.BATTERY_TEMP: Register("Battery Temp.", 0x331D, "Battery Temp.", C, 100),
    # Ambient Temp.
    RegisterTypeEnum.AMBIENT_TEMP: Register("Ambient Temp.", 0x331E, "Ambient Temp.", C, 100),

    # Setting Parameter (read-write) holding register
    # Battery Type
    RegisterTypeEnum.BATTERY_TYPE: Register("Battery Type", 0x9000, "0001H- Sealed , 0002H- GEL, 0003H- Flooded, 0000H- User defined", I, 1),
    # Battery Capacity
    RegisterTypeEnum.BATTERY_CAPACITY: Register("Battery Capacity", 0x9001, "Rated capacity of the battery", AH, 1),
    # Temperature compensation coefficient
    RegisterTypeEnum.TEMPERATURE_COMPENSATION_COEFFICIENT: Register("Temperature compensation coefficient", 0x9002, "Range 0-9 mV/°C/2V", I, 100),
    # High Volt.disconnect
    RegisterTypeEnum.HIGH_VOLT_DISCONNECT: Register("High Volt.disconnect", 0x9003, "High Volt.disconnect", V, 100),
    # Charging limit voltage
    RegisterTypeEnum.CHARGING_LIMIT_VOLTAGE: Register("Charging limit voltage", 0x9004, "Charging limit voltage", V, 100),
    # Over voltage reconnect
    RegisterTypeEnum.OVER_VOLTAGE_RECONNECT: Register("Over voltage reconnect", 0x9005, "Over voltage reconnect", V, 100),
    # Equalization voltage
    RegisterTypeEnum.EQUALIZATION_VOLTAGE: Register("Equalization voltage", 0x9006, "Equalization voltage", V, 100),
    # Boost voltage
    RegisterTypeEnum.BOOST_VOLTAGE: Register("Boost voltage", 0x9007, "Boost voltage", V, 100),
    # Float voltage
    RegisterTypeEnum.FLOAT_VOLTAGE: Register("Float voltage", 0x9008, "Float voltage", V, 100),
    # Boost reconnect voltage
    RegisterTypeEnum.BOOST_RECONNECT_VOLTAGE: Register("Boost reconnect voltage", 0x9009, "Boost reconnect voltage", V, 100),
    # Low voltage reconnect
    RegisterTypeEnum.LOW_VOLTAGE_RECONNECT: Register("Low voltage reconnect", 0x900A, "Low voltage reconnect", V, 100),
    # Under voltage recover
    RegisterTypeEnum.UNDER_VOLTAGE_RECOVER: Register("Under voltage recover", 0x900B, "Under voltage recover", V, 100),
    # Under voltage warning
    RegisterTypeEnum.UNDER_VOLTAGE_WARNING: Register("Under voltage warning", 0x900C, "Under voltage warning", V, 100),
    # Low voltage disconnect
    RegisterTypeEnum.LOW_VOLTAGE_DISCONNECT: Register("Low voltage disconnect", 0x900D, "Low voltage disconnect", V, 100),
    # Discharging limit voltage
    RegisterTypeEnum.DISCHARGING_LIMIT_VOLTAGE: Register("Discharging limit voltage", 0x900E, "Discharging limit voltage", V, 100),
    # Real time clock 1
    RegisterTypeEnum.REAL_TIME_CLOCK_1: Register("Real time clock 1", 0x9013, "D7-0 Sec, D15-8 Min.(Year,Month,Day,Min,Sec.should be writed simultaneously)", I, 1),
    # Real time clock 2
    RegisterTypeEnum.REAL_TIME_CLOCK_2: Register("Real time clock 2", 0x9014, "D7-0 Hour, D15-8 Day", I, 1),
    # Real time clock 3
    RegisterTypeEnum.REAL_TIME_CLOCK_3: Register("Real time clock 3", 0x9015, "D7-0 Month, D15-8 Year", I, 1),
    # Equalization charging cycle
    RegisterTypeEnum.EQUALIZATION_CHARGING_CYCLE: Register("Equalization charging cycle", 0x9016, "Interval days of auto equalization charging in cycle Day", I, 1),
    # Battery temperature warning upper limit
    RegisterTypeEnum.BATTERY_TEMPERATURE_WARNING_UPPER_LIMIT: Register("Battery temperature warning upper limit", 0x9017, "Battery temperature warning upper limit", C, 100),
    # Battery temperature warning lower limit
    RegisterTypeEnum.BATTERY_TEMPERATURE_WARNING_LOWER_LIMIT: Register("Battery temperature warning lower limit", 0x9018, "Battery temperature warning lower limit", C, 100),
    # Controller inner temperature upper limit
    RegisterTypeEnum.CONTROLLER_INNER_TEMPERATURE_UPPER_LIMIT: Register("Controller inner temperature upper limit", 0x9019, "Controller inner temperature upper limit", C, 100),
    # Controller inner temperature upper limit recover
    RegisterTypeEnum.CONTROLLER_INNER_TEMPERATURE_UPPER_LIMIT_RECOVER: Register("Controller inner temperature upper limit recover", 0x901A, "After Over Temperature, system recover once it drop to lower than this value", C, 100),
    # Power component temperature upper limit
    RegisterTypeEnum.POWER_COMPONENT_TEMPERATURE_UPPER_LIMIT: Register("Power component temperature upper limit", 0x901B, "Warning when surface temperature of power components higher than this value, and charging and discharging stop", C, 100),
    # Power component temperature upper limit recover
    RegisterTypeEnum.POWER_COMPONENT_TEMPERATURE_UPPER_LIMIT_RECOVER: Register("Power component temperature upper limit recover", 0x901C, "Recover once power components temperature lower than this value", C, 100),
    # Line Impedance
    RegisterTypeEnum.LINE_IMPEDANCE: Register("Line Impedance", 0x901D, "The resistance of the connectted wires.", MO, 100),
    # Night TimeThreshold Volt.(NTTV)
    RegisterTypeEnum.NIGHT_TIMETHRESHOLD_VOLT_NTTV: Register("Night TimeThreshold Volt.(NTTV)", 0x901E, " PV lower lower than this value, controller would detect it as sundown", V, 100),
    # Light signal startup (night) delay time
    RegisterTypeEnum.LIGHT_SIGNAL_STARTUP_NIGHT_DELAY_TIME: Register("Light signal startup (night) delay time", 0x901F, "PV voltage lower than NTTV, and duration exceeds the Light signal startup (night) delay time, controller would detect it as night time.", MIN, 1),
    # Day Time Threshold Volt.(DTTV)
    RegisterTypeEnum.DAY_TIME_THRESHOLD_VOLT_DTTV: Register("Day Time Threshold Volt.(DTTV)", 0x9020, "PV voltage higher than this value, controller would detect it as sunrise", V, 100),
    # Light signal turn off(day) delay time
    RegisterTypeEnum.LIGHT_SIGNAL_TURN_OFF_DAY_DELAY_TIME: Register("Light signal turn off(day) delay time", 0x9021, "PV voltage higher than DTTV, and duration exceeds Light signal turn off(day) delay time delay time, controller would detect it as daytime.", MIN, 1),
    # Load controling modes
    RegisterTypeEnum.LOAD_CONTROLING_MODES: Register("Load controling modes", 0x903D, "0000H Manual Control, 0001H Light ON/OFF, 0002H Light ON+ Timer/, 0003H Time Control", I, 1),
    # Working time length 1
    RegisterTypeEnum.WORKING_TIME_LENGTH_1: Register("Working time length 1", 0x903E, "The length of load output timer1, D15-D8,hour, D7-D0, minute", I, 1),
    # Working time length 2
    RegisterTypeEnum.WORKING_TIME_LENGTH_2: Register("Working time length 2", 0x903F, "The length of load output timer2, D15-D8, hour, D7-D0, minute", I, 1),
    # Turn on timing 1 sec
    RegisterTypeEnum.TURN_ON_TIMING_1_SEC: Register("Turn on timing 1 sec", 0x9042, "Turn on timing 1 sec", SEC, 1),
    # Turn on timing 1 min
    RegisterTypeEnum.TURN_ON_TIMING_1_MIN: Register("Turn on timing 1 min", 0x9043, "Turn on timing 1 min", MIN, 1),
    # Turn on timing 1 hour
    RegisterTypeEnum.TURN_ON_TIMING_1_HOUR: Register("Turn on timing 1 hour", 0x9044, "Turn on timing 1 hour", HOUR, 1),
    # Turn off timing 1 sec
    RegisterTypeEnum.TURN_OFF_TIMING_1_SEC: Register("Turn off timing 1 sec", 0x9045, "Turn off timing 1 sec", SEC, 1),
    # Turn off timing 1 min
    RegisterTypeEnum.TURN_OFF_TIMING_1_MIN: Register("Turn off timing 1 min", 0x9046, "Turn off timing 1 min", MIN, 1),
    # Turn off timing  hour
    RegisterTypeEnum.TURN_OFF_TIMING_1_HOUR: Register("Turn off timing 1 hour", 0x9047, "Turn off timing 1 hour", HOUR, 1),
    # Turn on timing 2 sec
    RegisterTypeEnum.TURN_ON_TIMING_2_SEC: Register("Turn on timing 2 sec", 0x9048, "Turn on timing 2 sec", SEC, 1),
    # Turn on timing 2 min
    RegisterTypeEnum.TURN_ON_TIMING_2_MIN: Register("Turn on timing 2 min", 0x9049, "Turn on timing 2 min", MIN, 1),
    # Turn on timing 2 hour
    RegisterTypeEnum.TURN_ON_TIMING_2_HOUR: Register("Turn on timing 2 hour", 0x904A, "Turn on timing 2 hour", HOUR, 1),
    # Turn off timing 2 sec
    RegisterTypeEnum.TURN_OFF_TIMING_2_SEC: Register("Turn off timing 2 sec", 0x904B, "Turn off timing 2 sec", SEC, 1),
    # Turn off timing 2 min
    RegisterTypeEnum.TURN_OFF_TIMING_2_MIN: Register("Turn off timing 2 min", 0x904C, "Turn off timing 2 min", MIN, 1),
    # Turn off timing 2 hour
    RegisterTypeEnum.TURN_OFF_TIMING_2_HOUR: Register("Turn off timing 2 hour", 0x904D, "Turn off timing 2 hour", HOUR, 1),
    # Length of night
    RegisterTypeEnum.LENGTH_OF_NIGHT: Register("Length of night", 0x9065, "Set default values of the whole night length of time. D15-D8,hour, D7-D0, minute", I, 1),
    # Battery rated voltage code
    RegisterTypeEnum.BATTERY_RATED_VOLTAGE_CODE: Register("Battery rated voltage code", 0x9067, "0, auto recognize. 1-12V, 2-24V", I, 1),
    # Load timing control selection
    RegisterTypeEnum.LOAD_TIMING_CONTROL_SELECTION: Register("Load timing control selection", 0x9069, "Selected timeing period of the load.0, using one timer, 1-using two timer, likewise.", I, 1),
    # Default Load On/Off in manual mode
    RegisterTypeEnum.DEFAULT_LOAD_ON_OFF_IN_MANUAL_MODE: Register("Default Load On/Off in manual mode", 0x906A, "0-off, 1-on", I, 1),
    # Equalize duration
    RegisterTypeEnum.EQUALIZE_DURATION: Register("Equalize duration", 0x906B, "Usually 60-120 minutes.", MIN, 1),
    # Boost duration
    RegisterTypeEnum.BOOST_DURATION: Register("Boost duration", 0x906C, "Usually 60-120 minutes.", MIN, 1),
    # Discharging percentage
    RegisterTypeEnum.DISCHARGING_PERCENTAGE: Register("Discharging percentage", 0x906D, "Usually 20%-80%. The percentage of battery's remaining capacity when stop charging", PC, 1),
    # Charging percentage
    RegisterTypeEnum.CHARGING_PERCENTAGE: Register("Charging percentage", 0x906E, "Depth of charge, 20%-100%.", PC, 1),
    # 906f?
    # Management modes of battery charging and discharging
    RegisterTypeEnum.MANAGEMENT_MODES_OF_BATTERY_CHARGING_AND_DISCHARGING: Register("Management modes of battery charging and discharging", 0x9070, "Management modes of battery charge and discharge, voltage compensation : 0 and SOC : 1.", I, 1),
}

coils = {
    # Coils(read-write)
    # Manual control the load
    CoilTypeEnum.MANUAL_CONTROL_THE_LOAD: Coil("Manual control the load", 2, "When the load is manual mode, 1-manual on, 0 -manual off", I, 1),
    # Enable load test mode
    CoilTypeEnum.ENABLE_LOAD_TEST_MODE: Coil("Enable load test mode", 5, "1 Enable, 0 Disable(normal)", I, 1),
    # Force the load on/off
    CoilTypeEnum.FORCE_THE_LOAD_ON_OFF: Coil("Force the load on/off", 6, "1 Turn on, 0 Turn off (used for temporary test of the load)", I, 1),

    # Discrete input (read-only)
    # Over temperature inside the device
    CoilTypeEnum.OVER_TEMPERATURE_INSIDE_THE_DEVICE: Coil("Over temperature inside the device", 0x2000, "1 The temperature inside the controller is higher than the over-temperature protection point. 0 Normal", I, 1),
    # Day/Night
    CoilTypeEnum.DAY_NIGHT: Coil("Day/Night", 0x200C, "1-Night, 0-Day", I, 1),
}

# RJ45 pinout
# 1, 2- No connected
# 3, 4- RS-485 A
# 5, 6- RS-485 B
# 7, 8- Ground
# The pins define for the RJ-45 port of LS-B controller. Pin 3 and 4 is the A of RS-485, Pin 5 and 6 is B.
#
# (1) To improve the communication quality, the ground pins 7 and 8 (connected with the negative terminal of
# the battery) could be used if necessary. However, the user must care the common ground problem of the
# connected devices.
# (2) User is advised to do not use the pin 1 and pin 2 for the device's safety

_registerByName = {}

for register_type, reg in registers.items():
    name = reg.name
    if name in _registerByName:
        raise Exception("internal error " + name)
    _registerByName[name] = reg

for register_type, reg in coils.items():
    name = reg.name
    if name in _registerByName:
        raise Exception("internal error " + name)
    _registerByName[name] = reg


def registerByName(name):
    if name not in _registerByName:
        raise Exception("Unknown register " + repr(name))
    return _registerByName[name]


__all__ = [
    "registers",
    "coils",
    "registerByName",
]
