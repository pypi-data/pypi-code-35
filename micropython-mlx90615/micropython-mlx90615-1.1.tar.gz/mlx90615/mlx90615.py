
from machine import I2C, Pin
import time


from . import crc8


def pec(bytearray_):
    
    pec_ = crc8.crc8()
    pec_.update(bytes(bytearray_))
    
    return int(pec_.hexdigest(), 16)


########################################################################
class MLX90615:
    ADDR = 0x5b
    EEPROM = 0x10
    RAM = 0x20
    
    TA = 0x06
    TO = 0x07
    
    PWM_TMIN__SMBUS_SA = 0x00
    PWM_T_RANGE = 0x01
    CONFIG = 0x02
    EMISSIVITY = 0x03

    
    
    # ----------------------------------------------------------------------
    def __init__(self, sda, scl):
        """"""
        self.i2c = I2C(scl=Pin(scl), sda=Pin(sda)) 
        
           
    # ----------------------------------------------------------------------
    def read_eeprom(self, reg):
        """"""
        a, b, _pec = self.i2c.readfrom_mem(self.ADDR, reg|self.EEPROM, 3)
        return int(hex(b) + hex(a)[2:], 16)
        # return a, b
        
    # ----------------------------------------------------------------------
    def bin_(self, value):
        """"""
        value = bin(value)[2:]
        ljust = 16
        return list('0' * max(0, ljust - len(value)) + value)
        
    # ----------------------------------------------------------------------
    def divmode(self, value):
        """"""
        return value//256, value % 256
        
        
    # ----------------------------------------------------------------------
    def bytes_(self, value):
        """"""
        # return (value).to_bytes(2, 'big')  
        return bytes(reversed((value).to_bytes(2, 'big') ))   
        
    # ----------------------------------------------------------------------
    def is_pwm(self):
        """"""
        config = self.read_eeprom(self.CONFIG)
        return self.bin_(config)[-1] == '0'
        
    # ----------------------------------------------------------------------      
    def read_temp(self, reg=TO):
        """"""
        a, b = self.i2c.readfrom_mem(self.ADDR, reg|self.RAM, 2)
        temp = int(hex(b) + hex(a)[2:], 16)
    
        temp *= .02 
        temp  -= 273.15
        return round(temp, 2)
    
    # ----------------------------------------------------------------------
    def __getattr__(self, attr):
        """"""
        if hasattr(self.i2c, attr):
            return getattr(self.i2c, attr)
            
    # ----------------------------------------------------------------------
    def set_pwm_mode(self, mode=True):
        """"""
        config = self.read_eeprom(self.CONFIG)
        config_ = self.bin_(config)
        
        if mode: 
            config_[-1] = '0'
        else:
            config_[-1] = '1'
             
        reg = int('0b' + ''.join(config_), 2)
        
        self.write_eeprom(self.CONFIG, reg)
        
    # ----------------------------------------------------------------------
    def write_eeprom(self, reg, value):
        """"""
        if self.read_eeprom(reg) == value:
            return
        
        self._write_eeprom(reg, 0x0000)
        time.sleep_ms(10)
        self._write_eeprom(reg, value)
        time.sleep_ms(10)
        
    # ----------------------------------------------------------------------
    def _write_eeprom(self, reg, value):
        """"""
        buff = bytearray(5)
        buff[0] = self.ADDR<<1
        buff[1] = reg|self.EEPROM 
        buff[2] = self.divmode(value)[1]
        buff[3] = self.divmode(value)[0]
        buff[4] = pec(buff[:4])
        
        self.i2c.writeto_mem(self.ADDR, reg|self.EEPROM, bytes(buff[-3:]))
        
        return hex(buff[4])
      
      

