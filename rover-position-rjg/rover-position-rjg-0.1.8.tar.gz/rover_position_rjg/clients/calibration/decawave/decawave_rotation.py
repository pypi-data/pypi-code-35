from rover_position_rjg.data.quaternion import Quaternion
from rover_position_rjg.data.vector import Vector

if __name__ == '__main__':
    # base is angle between base line (anchor 0 to anchor 1) and North
    base = 74
    # rotation angle
    theta = 90 - base
    q = Quaternion.from_euler(Vector([0.0, 0.0, theta]))
    print('decawave_calibration.json is:')
    print('{{"rotation":{}}}'.format(q.to_json()))
