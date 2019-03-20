import math

from rover_position_rjg.data.vector import Vector
from rover_position_rjg.position.calibration.decawave.anchor_ranges_to_positions import AnchorRangesToPositions


def get_leading_diagonal_coord(layout: AnchorRangesToPositions, dist: float):
    diag_1_3 = math.sqrt(layout.position_3().x**2 + layout.position_3().y**2)
    ratio = dist/diag_1_3
    return [ratio * layout.position_3().x, ratio * layout.position_3().y]


def get_trailing_diagonal_coord(layout: AnchorRangesToPositions, dist: float):
    delta = layout.position_2() - layout.position_4()
    diag_2_4 = math.sqrt(delta.x**2 + delta.y**2)
    ratio = dist/diag_2_4
    x = layout.position_4().x + (layout.position_2().x * (1 - ratio))
    y = layout.position_4().y * ratio
    return [x, y]


def get_distances(layout: AnchorRangesToPositions, position: Vector):
    d0 = (layout.position_1() - position).magnitude()
    d1 = (layout.position_2() - position).magnitude()
    d2 = (layout.position_3() - position).magnitude()
    d3 = (layout.position_4() - position).magnitude()
    return [d0, d1, d2, d3]


if __name__ == '__main__':
    side_0_1 = 3520
    side_1_2 = 3460
    side_2_3 = 3251
    side_3_0 = 3362
    diag_0_2 = 4789
    diag_1_3 = 4818
    height = 420
    rover_height = 250

    layout = AnchorRangesToPositions(
        side_0_1, side_1_2, side_2_3, side_3_0,
        diag_0_2, diag_1_3, height
    )
    print('0 - {}'.format(layout.position_1()))
    print('1 - {}'.format(layout.position_2()))
    print('2 - {}'.format(layout.position_3()))
    print('3 - {}'.format(layout.position_4()))
    print('Diag 1/3 error {:.2f}'.format(layout.error_3_4()))

    # Leading diagonal co-ordinates
    print()
    print('Leading Diagonal')
    for i in range(1000, int(diag_0_2), 1000):
        diag = get_leading_diagonal_coord(layout, i)
        distances = get_distances(layout, Vector([diag[0], diag[1], rover_height]))
        print('Diag 0->2, {}mm [{:4.0f}, {:4.0f}], Ranges [{:4.0f}, {:4.0f}, {:4.0f}, {:4.0f}]'.format(
            i, diag[0], diag[1], distances[0], distances[1], distances[2], distances[3]))

    print()
    print('Trailing Diagonal')
    for i in range(1000, int(diag_1_3), 1000):
        diag = get_trailing_diagonal_coord(layout, i)
        distances = get_distances(layout, Vector([diag[0], diag[1], rover_height]))
        print('Diag 1->3, {}mm [{:4.0f}, {:4.0f}], Ranges [{:4.0f}, {:4.0f}, {:4.0f}, {:4.0f}]'.format(
            i, diag[0], diag[1], distances[0], distances[1], distances[2], distances[3]))


