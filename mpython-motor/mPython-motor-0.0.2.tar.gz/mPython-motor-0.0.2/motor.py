from mpython import i2c


class Motor(object):
    """
    I2C通讯控制驱动电机类

    :param i2c: I2C实例对象，默认i2c=i2c

    """

    def __init__(self, i2c=i2c):
        self.i2c = i2c
        self._buf = {}

    def set_speed(self, motor_no, spend):
        """
        设置电机速度

        :param int motor_no: 控制电机编号，可以使用 :py:meth:`MOTOR_1<Motor.MOTOR_1>`, :py:meth:`MOTOR_2<Motor.MOTOR_2>` ,或者直接写入电机编号。
        :param int speed: 电机速度，范围-100~100，负值代表反转。

        """
        speed = max(min(spend, 100), -100)
        self._buf.update({motor_no: spend})
        self.i2c.writeto(0x10, bytearray([motor_no, speed]))

    def get_speed(self, motor_no):
        """
        返回电机速度

        :param int motor_no: 控制电机编号，可以使用 :py:meth:`MOTOR_1<Motor.MOTOR_1>`, :py:meth:`MOTOR_2<Motor.MOTOR_2>`,或者直接写入电机编号。
        :rtype: int
        :return: 返回该电机速度
        """
        if motor_no in self._buf:

            return self._buf[motor_no]
        else:
            return None

    MOTOR_1 = 0x01
    """
    M1电机常量，0x01
    """

    MOTOR_2 = 0x02
    """
    M2电机常量，0x02
    """
