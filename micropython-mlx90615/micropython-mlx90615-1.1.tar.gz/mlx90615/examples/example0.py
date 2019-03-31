from mlx90615 import MLX90615
from espresso import print_ as print
from oled.lazy import Oled_i2c, ubuntu_mono_15
from machine import Pin
import time

mlx = MLX90615(sda=21, scl=22)
oled = Oled_i2c(sda=4, scl=15)
button = Pin(0, Pin.IN)
led = Pin(2, Pin.OUT, value=0)


data = {
'CONFIG': hex(mlx.read_eeprom(mlx.CONFIG)),
'MODE': {0: 'I2C', 1:'PWM'}[mlx.is_pwm()],
'TEMP-To': mlx.read_temp(mlx.TO),
'TEMP-Ta': mlx.read_temp(mlx.TA),
}

def show_config():
    oled.fill(0)
    line = 0
    for k in data:
        oled.write("{}: {}".format(k, data[k]), (0, line), ubuntu_mono_15)
        line += 12
    oled.show()


def get_button():
    led.value(1)
    while button.value() == 1:
        pass
    
    t0 = time.time()
    def t():
        return time.time()-t0
    
    action = 0
    while button.value() == 0:
        if action != 0:
            break
        # print('IN-0')
        if t()>2:
            print('IN-1')
            action = 1
            while (button.value() == 0) and (t()<6):
                led.value(1)
                time.sleep_ms(100)
                led.value(0)
                time.sleep_ms(100)
                
            while button.value() == 0:
              
                if t()>6:
                    print('IN-2')
                    action = 2
                    while (button.value() == 0) and (t()<10):
                        led.value(1)
                        time.sleep_ms(200)
                        led.value(0)
                        time.sleep_ms(200)
         
    led.value(0)
    return action

 

while True:
    show_config()
    action = get_button()
    
    if action == 0:
        print('ACTION-0')
    elif action == 1:
        print('ACTION-1')
    elif action == 2:
        print('ACTION-2')
        
    time.sleep_ms(500)
        
        







