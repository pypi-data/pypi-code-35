import re
from typing import List

from rover_position_rjg.data.data import Data
from rover_position_rjg.data.vector import Vector
from rover_position_rjg.sensors.imu.nine_dof_data import NineDoFData


class Calibrate:
    def __init__(self):
        self.x_plus_south: NineDoFData = None
        self.x_minus_south: NineDoFData = None
        self.y_plus_south: NineDoFData = None
        self.y_minus_south: NineDoFData = None
        self.z_plus_south: NineDoFData = None
        self.z_minus_south: NineDoFData = None
        self.offsets = NineDoFData.zero()
        self.offsets.temperature.value = -440
        self.multipliers = NineDoFData.one()
        self.multipliers.temperature.value = 0.0625

    def set_gyro_offset(self):
        total_gyro = Vector.zero()
        total_gyro += self.x_plus_south.angular_velocity.value
        total_gyro += self.x_minus_south.angular_velocity.value
        total_gyro += self.y_plus_south.angular_velocity.value
        total_gyro += self.y_plus_south.angular_velocity.value
        total_gyro += self.z_minus_south.angular_velocity.value
        total_gyro += self.z_plus_south.angular_velocity.value
        self.offsets.angular_velocity.value = total_gyro / 6
        print("Gyro offset: {}".format(self.offsets.angular_velocity.value))

    def set_accelerometer_offset_and_multiplier(self):
        g = 1
        offsets = [0, 0, 0]
        multipliers = [0, 0, 0]
        # x
        x_max = self.x_plus_south.acceleration.value
        x_min = self.x_minus_south.acceleration.value
        offsets[0] = self._get_average(x_max.x, x_min.x)
        multipliers[0] = self._get_scaling(x_min.x, x_max.x, g)
        # y
        y_max = self.y_plus_south.acceleration.value
        y_min = self.y_minus_south.acceleration.value
        offsets[1] = self._get_average(y_max.y, y_min.y)
        multipliers[1] = self._get_scaling(y_min.y, y_max.y, g)
        # z
        z_max = self.z_plus_south.acceleration.value
        z_min = self.z_minus_south.acceleration.value
        offsets[2] = self._get_average(z_max.z, z_min.z)
        multipliers[2] = self._get_scaling(z_min.z, z_max.z, g)
        # save results
        print("Acc: {}, {}".format(offsets, multipliers))
        self.offsets.acceleration.value = Vector(offsets)
        self.multipliers.acceleration.value = Vector(multipliers)

    def set_magnetometer_offset_and_multiplier(self):
        offsets = [0, 0, 0]
        multipliers = [0, 0, 0]
        # x
        x_max = self.x_plus_south.magnetic_field.value
        x_min = self.x_minus_south.magnetic_field.value
        offsets[0] = self._get_average(x_max.x, x_min.x)
        # multipliers[0] = self._get_scaling(x_min.x, x_max.x, g)
        # y
        y_max = self.y_plus_south.magnetic_field.value
        y_min = self.y_minus_south.magnetic_field.value
        offsets[1] = self._get_average(y_max.y, y_min.y)
        # multipliers[1] = self._get_scaling(y_min.y, y_max.y, g)
        # z
        z_max = self.z_plus_south.magnetic_field.value
        z_min = self.z_minus_south.magnetic_field.value
        offsets[2] = self._get_average(z_max.z, z_min.z)
        # multipliers[2] = self._get_scaling(z_min.z, z_max.z, g)
        # save results
        print("Mag: {}, {}".format(offsets, multipliers))
        self.offsets.magnetic_field.value = Vector(offsets)
        self.multipliers.magnetic_field.value = Vector(multipliers)

    def print(self):
        data = '{{\n"offset":{},\n"multiplier":{}\n}}'.format(self.offsets.to_json(), self.multipliers.to_json())
        print(data)

    @staticmethod
    def _get_scaling(min: float, max: float, value: float) -> float:
        return (value * 2)/(max - min)

    @staticmethod
    def _get_average(a: float, b: float) -> float:
        return (a + b) / 2

    def set_x_plus_south(self, value_pair: List[str]):
        self.x_plus_south = Calibrate.pair_to_nine_dof(value_pair)

    def set_x_minus_south(self, value_pair: List[str]):
        self.x_minus_south = Calibrate.pair_to_nine_dof(value_pair)

    def set_y_plus_south(self, value_pair: List[str]):
        self.y_plus_south = Calibrate.pair_to_nine_dof(value_pair)

    def set_y_minus_south(self, value_pair: List[str]):
        self.y_minus_south = Calibrate.pair_to_nine_dof(value_pair)

    def set_z_plus_south(self, value_pair: List[str]):
        self.z_plus_south = Calibrate.pair_to_nine_dof(value_pair)

    def set_z_minus_south(self, value_pair: List[str]):
        self.z_minus_south = Calibrate.pair_to_nine_dof(value_pair)

    @staticmethod
    def pair_to_nine_dof(value_pair: List[str]):
        a = Calibrate.parse_line(value_pair[0])
        b = Calibrate.parse_line(value_pair[1])
        return (a + b) / 2

    @staticmethod
    def parse_line(line: str) -> NineDoFData:
        values = re.findall(r"-?[\d]+", line)
        acc = Calibrate._to_vector(values[0:3])
        gyro = Calibrate._to_vector(values[3:6])
        mag = Calibrate._to_vector(values[6:9])
        temp = int(values[9])
        t = 1
        return NineDoFData(Data(acc, t), Data(gyro, t), Data(mag, t), Data(temp, t))

    @staticmethod
    def _to_vector(values: List[str]) -> Vector:
        return Vector([int(values[0]), int(values[1]), int(values[2])])


if __name__ == '__main__':
    calibrator = Calibrate()

    # Min/Max Z
    # calibrator.set_z_plus_south([
    #     "838    155  16276 |   -361    -48    176 |   1344   1008  -2584 |  -122",
    #     "412    -51  16281 |   -361    -46    175 |   1330   3594  -2556 |  -122"
    # ])
    # calibrator.set_z_minus_south([
    #     "410   -160 -16410 |   -368    -50    178 |   1273   3599   3125 |  -123",
    #     "-172    154 -16374 |   -373    -55    172 |   1538   1079   3244 |  -114"
    # ])
    # # Min/Max X
    # calibrator.set_x_plus_south([
    #     "16764    384   -704 |   -370    -52    173 |  -1616   3606    561 |  -114",
    #     "16695    665  -1545 |   -372    -53    174 |  -1483    996    737 |  -112"
    # ])
    # calibrator.set_x_minus_south([
    #     "-16033   -505    861 |   -369    -53    174 |   4388   1042     87 |  -112",
    #     "-16045   -721    331 |   -370    -39    174 |   4180   3646    234 |  -113"
    # ])
    # # Min/Max Y
    # calibrator.set_y_plus_south([
    #     "-471  16359   -515 |   -379    -62    173 |   2944   -663    363 |  -105",
    #     "-211  16365    345 |   -383    -54    171 |    273   -685    467 |   -99"
    # ])
    # calibrator.set_y_minus_south([
    #     "1974 -16331   -385 |   -394    -55    167 |   -298   5178    616 |   -85",
    #     "1780 -16314  -1134 |   -366    -55    165 |   2164   5383    432 |   -91"
    # ])
    calibrator.set_z_plus_south([
        "766     39  16145 |   -524    -91    106 |   -374   3759   -761 |   101",
        "585    179  16152 |   -516    -90    110 |    -16   1276   -710 |    91"
    ])
    calibrator.set_z_minus_south([
        "655    -71 -16531 |   -532    -92    124 |     21   1014   5465 |   100",
        "543   -111 -16532 |   -535    -92    123 |     -4   3636   5219 |   101"
    ])
    # Min/Max X
    calibrator.set_x_plus_south([
        "17004    118   -891 |   -635   -395    124 |  -2832   4455   3866 |    94",
        "16930    251     42 |   -516   -110    105 |  -2951   2418   3599 |    88"
    ])
    calibrator.set_x_minus_south([
        "-15843   -120    -90 |   -456    -90    125 |   3122   1782   5373 |    92",
        "-15854   -176   -294 |   -532   -101    122 |   2741   1910   3182 |   102"
    ])
    # Min/Max Y
    calibrator.set_y_plus_south([
        "518  16420   -244 |   -515    -93    129 |    244    417   2153 |    82",
        "325  16407    262 |   -522     72    141 |    538    324   4616 |    81"
    ])
    calibrator.set_y_minus_south([
        "812 -16340    -69 |   -532    -92    125 |    209   5264   3570 |   105",
        "672 -16344    -23 |   -515   -135    124 |    362   5395    819 |    99"
    ])

    calibrator.set_gyro_offset()
    calibrator.set_accelerometer_offset_and_multiplier()
    calibrator.set_magnetometer_offset_and_multiplier()
    calibrator.print()
