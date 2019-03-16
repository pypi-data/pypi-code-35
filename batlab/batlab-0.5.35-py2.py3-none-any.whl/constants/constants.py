# namespace definitions
CELL0             = 0x00
CELL1             = 0x01
CELL2             = 0x02
CELL3             = 0x03
UNIT              = 0x04
BOOTLOADER        = 0x05
COMMS             = 0xFF
NAMESPACE_LIST = [0x00,0x01,0x02,0x03,0x04,0x05,0xFF]

# cell register map
MODE              = 0x00
ERROR             = 0x01
STATUS            = 0x02
CURRENT_SETPOINT  = 0x03
REPORT_INTERVAL   = 0x04
TEMPERATURE       = 0x05
CURRENT           = 0x06
VOLTAGE           = 0x07
CHARGEL           = 0x08
CHARGEH           = 0x09
VOLTAGE_LIMIT_CHG = 0x0A
VOLTAGE_LIMIT_DCHG= 0x0B
CURRENT_LIMIT_CHG = 0x0C
CURRENT_LIMIT_DCHG= 0x0D
TEMP_LIMIT_CHG    = 0x0E
TEMP_LIMIT_DCHG   = 0x0F
DUTY              = 0x10
COMPENSATION      = 0x11
CURRENT_PP        = 0x12
VOLTAGE_PP        = 0x13
CURRENT_CALIB_OFF = 0x14
CURRENT_CALIB_SCA = 0x15
TEMP_CALIB_R      = 0x16
TEMP_CALIB_B      = 0x17
CURRENT_CALIB_PP  = 0x18
VOLTAGE_CALIB_PP  = 0x19
CURR_CALIB_PP_OFF = 0x1A
VOLT_CALIB_PP_OFF = 0x1B
CURR_LOWV_SCA     = 0x1C
CURR_LOWV_OFF     = 0x1D
CURR_LOWV_OFF_SCA = 0x1E

CELLREG_MAX = 0x1E

# unit register map
SERIAL_NUM       =  0x00
DEVICE_ID        =  0x01
FIRMWARE_VER     =  0x02
VCC              =  0x03
SINE_FREQ        =  0x04
SYSTEM_TIMER     =  0x05
SETTINGS         =  0x06
SINE_OFFSET      =  0x07
SINE_MAGDIV      =  0x08
LED_MESSAGE      =  0x09
BOOTLOAD         =  0x0A
VOLT_CH_CALIB_OFF = 0x0B
VOLT_CH_CALIB_SCA = 0x0C
VOLT_DC_CALIB_OFF = 0x0D
VOLT_DC_CALIB_SCA = 0x0E
LOCK              = 0x0F
ZERO_AMP_THRESH   = 0x10
WATCHDOG_TIMER    = 0x11

UNITREG_MAX = 0x11

# COMMs register map
LED0             = 0x00
LED1             = 0x01
LED2             = 0x02
LED3             = 0x03
PSU              = 0x04
PSU_VOLTAGE      = 0x05

COMMREGS_MAX = 0x05

# BOOTLOAD register map
BL_BOOTLOAD      = 0x00
BL_ADDR          = 0x01
BL_DATA          = 0x02

# register specific codes and defines
MODE_NO_CELL           = 0x0000
MODE_BACKWARDS         = 0x0001
MODE_IDLE              = 0x0002
MODE_CHARGE            = 0x0003
MODE_DISCHARGE         = 0x0004
MODE_IMPEDANCE         = 0x0005
MODE_STOPPED           = 0x0006
MODE_LIST = ['MODE_NO_CELL','MODE_BACKWARDS','MODE_IDLE','MODE_CHARGE','MODE_DISCHARGE','MODE_IMPEDANCE','MODE_STOPPED']
ERR_VOLTAGE_LIMIT_CHG  = 0x0001
ERR_VOLTAGE_LIMIT_DCHG = 0x0002
ERR_CURRENT_LIMIT_CHG  = 0x0004
ERR_CURRENT_LIMIT_DCHG = 0x0008
ERR_TEMP_LIMIT_CHG     = 0x0010
ERR_TEMP_LIMIT_DCHG    = 0x0020
ERR_BACKWARDS          = 0x0040
ERR_NO_CELL            = 0x0080
ERR_NO_PSU             = 0x0100
ERR_LOW_VCC            = 0x0800
ERR_LIST = ['ERR_VOLTAGE_LIMIT_CHG','ERR_VOLTAGE_LIMIT_DCHG','ERR_CURRENT_LIMIT_CHG','ERR_CURRENT_LIMIT_DCHG','ERR_TEMP_LIMIT_CHG','ERR_TEMP_LIMIT_DCHG','ERR_BACKWARDS','ERR_NO_CELL','ERR_NO_PSU','','','ERR_LOW_VCC']
STAT_VOLTAGE_LIMIT_CHG = 0x0001
STAT_VOLTAGE_LIMIT_DCHG= 0x0002
STAT_CURRENT_LIMIT_CHG = 0x0004
STAT_CURRENT_LIMIT_DCHG= 0x0008
STAT_TEMP_LIMIT_CHG    = 0x0010
STAT_TEMP_LIMIT_DCHG   = 0x0020
STAT_BACKWARDS         = 0x0040
STAT_NO_CELL           = 0x0080
STAT_NO_PSU            = 0x0100
STAT_NOT_INITIALIZED   = 0x0200
STAT_NOT_CALIBRATED    = 0x0400
STAT_LOW_VCC           = 0x0800
SET_TRIM_OUTPUT        = 0x0001
SET_VCC_COMPENSATION   = 0x0002
SET_WATCHDOG_TIMER     = 0x0004
SET_CH0_HI_RES         = 0x0010
SET_NO_PSU_DCHG_ENABLE = 0x0008
SET_DEBUG              = 0x8000
LED_OFF                = 0x0000
LED_BLIP               = 0x0001
LED_FLASH_SLOW         = 0x0002
LED_FLASH_FAST         = 0x0003
LED_ON                 = 0x0004
LED_PWM                = 0x0005
LED_RAMP_UP            = 0x0006
LED_RAMP_DOWN          = 0x0007
LED_SINE               = 0x0008
WDT_RESET              = 255

LOCK_LOCKED            = 0x0001
LOCK_UNLOCKED          = 0x0000

COMMAND_ERROR          = 257

# test manager constants
TT_DISCHARGE = 0
TT_CYCLE = 1

TS_IDLE          = 0
TS_CHARGE        = 1
TS_PRECHARGE     = 2
TS_DISCHARGE     = 3
TS_CHARGEREST    = 4
TS_DISCHARGEREST = 5
TS_POSTDISCHARGE = 6
l_test_state= ["IDLE","CHARGE","PRECHARGE","DISCHARGE","CHARGEREST","DISCHARGEREST","POSTDISCHARGE"]
