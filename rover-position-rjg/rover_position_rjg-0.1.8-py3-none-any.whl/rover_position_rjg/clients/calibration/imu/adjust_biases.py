from rover_position_rjg.clients.calibration.imu.imu_calibrator import ImuCalibrator
from rover_position_rjg.data.vector import Vector
from rover_position_rjg.position.calibration.simple_scaler import SimpleScaler
from rover_position_rjg.sensors.imu.nine_dof_data import NineDoFData


def unscale(scaled_value: Vector, multiplier: Vector) -> Vector:
    inv_multiplier = Vector([1/multiplier.x, 1/multiplier.y, 1/multiplier.z])
    return scaled_value.scale(inv_multiplier)


if __name__ == '__main__':
    scaler = SimpleScaler(NineDoFData.zero(), NineDoFData.one())
    # scaler.load('../../../imu_calibration.json')
    calibrator = ImuCalibrator(scaler.offset, scaler.multiplier)

    # Set accelerations
    # # 25C
    # a0 = (
    #     Vector([155, -152, 16420]),
    #     Vector([679, 96, 16415])
    # )
    # a1 = (
    #     Vector([300, 235, 16414]),
    #     Vector([553, -290, 16423])
    # )

    # 26C -23
    # a0 = (
    #     Vector([515, 55, 16424]),
    #     Vector([341, -186, 16420])s
    # )
    # a1 = (
    #     Vector([320, 3, 16419]),
    #     Vector([571, -133, 16416])
    # )

    # 23C -73
    # a0 = (
    #     Vector([346, 97, 16423]),
    #     Vector([486, -182, 16422])
    # )
    # a1 = (
    #     Vector([288, -109, 16425]),
    #     Vector([575, 22, 16424])
    # )

    # calibrator.set_x_y_acceleration_biases([a0, a1])
    # calibrator.set_acceleration_biases_to_1_g(a1[1])
    # print('Acc: {}'.format(calibrator.offsets.acceleration.value))

    # m0 = (
    #     Vector([-210, 2456, -2212]),
    #     Vector([2471, 2227, -2394])
    # )
    # m1 = (
    #     Vector([1190, 3632, -2294]),
    #     Vector([1037, 1037, -2348])
    # )


    m0 = (
        Vector([220, 630, 7113]),
        Vector([79, 3177, 7048])
    )
    m1 = (
        Vector([-1220, 1945, 7083]),
        Vector([1377, 1853, 7050])
    )
    calibrator.set_x_y_magnetic_field_biases([m0, m1])
    print('Mag: {}'.format(calibrator.offsets.magnetic_field.value))
