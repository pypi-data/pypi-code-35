# from espresso import print_ as print
import time
from mlx90615 import MLX90615

mlx = MLX90615(sda=21, scl=22)


def update():
    data = {
        'CONFIG': hex(mlx.read_eeprom(mlx.CONFIG)),
        'MODE': {0: 'I2C', 1: 'PWM'}[mlx.is_pwm()],
        'TEMP-To': mlx.read_temp(mlx.TO),
        'TEMP-Ta': mlx.read_temp(mlx.TA),
    }

    print('\n' + '#' * 30)
    for k in data:
        print("{}: {}".format(k, data[k]))


for i in range(20):
    update()
    time.sleep_ms(500)

