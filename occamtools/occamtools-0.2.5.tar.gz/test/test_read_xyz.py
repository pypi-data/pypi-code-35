import os
import pytest
import numpy as np
from occamtools.read_xyz import Xyz, _are_floats

file_name = os.path.join(os.path.dirname(__file__), os.pardir, 'data',
                         'example_fort.8')


def _read_default_file_name():
    xyz = Xyz(file_name)
    xyz.read_file(silent=True)
    return xyz


def test_read_xyz_file():
    other_file = os.path.join(os.path.dirname(__file__), os.pardir, 'data',
                              'example_fort.5')
    xyz = Xyz(file_name)
    xyz.read_file(silent=True)
    assert xyz.x.shape == (12, 25)

    del xyz
    xyz = Xyz(other_file)
    caught = False
    try:
        xyz.read_file(silent=True)
    except ValueError:
        caught = True
    assert caught

    del xyz
    xyz = Xyz(other_file)
    xyz.read_file(file_name, silent=True)
    assert xyz.y.shape == (12, 25)


def test_read_xyz_types():
    xyz = _read_default_file_name()
    assert 'Ar' in xyz.type_dict
    assert xyz.type_dict['Ar'] == 0
    assert np.squeeze(xyz.type).shape == (25,)
    assert all([(i == 0) for i in xyz.type])


def test_read_xyz_positions():
    xyz = _read_default_file_name()
    assert xyz.x[0, 6] == pytest.approx(6.7048148063, abs=1e-9)
    assert xyz.x[2, 18] == pytest.approx(7.9447518060, abs=1e-9)
    assert xyz.x[8, 15] == pytest.approx(6.5780688198, abs=1e-9)

    assert xyz.y[0, 6] == pytest.approx(1.6830535784, abs=1e-9)
    assert xyz.y[2, 18] == pytest.approx(3.9503403522, abs=1e-9)
    assert xyz.y[8, 15] == pytest.approx(4.9175769932, abs=1e-9)

    assert xyz.z[0, 6] == pytest.approx(4.4030514961, abs=1e-9)
    assert xyz.z[2, 18] == pytest.approx(1.5187645491, abs=1e-9)
    assert xyz.z[8, 15] == pytest.approx(3.3215257040, abs=1e-9)


def test_read_xyz_time_array():
    xyz = _read_default_file_name()
    assert np.squeeze(xyz.time).shape == (12,)
    assert xyz.time[0] == pytest.approx(0, abs=1e-9)
    assert xyz.time[1] == pytest.approx(0.03, abs=1e-9)
    assert xyz.time[2] == pytest.approx(0.3, abs=1e-9)
    assert xyz.time[11] == pytest.approx(3.0, abs=1e-9)


def test_read_xyz_parse_comment_line():
    xyz = _read_default_file_name()
    xyz._parse_comment_first('1.7 2.5 5.0 5.0')
    assert xyz.comment_format_known
    assert xyz.time[0] == pytest.approx(1.7, abs=1e-15)
    assert np.allclose(xyz.box, [2.5, 5.0, 5.0])

    del xyz
    xyz = _read_default_file_name()
    time_0 = 985.2519859185
    xyz.time[0] = time_0
    xyz._parse_comment_first('6.7 8.1 9.9')
    assert xyz.comment_format_known is False
    assert xyz.time[0] == time_0
    assert np.allclose(xyz.box, [6.7, 8.1, 9.9])

    del xyz
    xyz = _read_default_file_name()
    xyz._parse_comment_first('abc')
    assert xyz.comment_format_known is False
    assert all([b is None for b in xyz.box])

    del xyz
    xyz = _read_default_file_name()
    xyz._parse_comment_first('1.0 2.0 A')
    assert xyz.comment_format_known is False
    assert all([b is None for b in xyz.box])

    del xyz
    xyz = _read_default_file_name()
    xyz._parse_comment_first('1.0 2.0 3.0 B')
    assert xyz.comment_format_known is False
    assert all([b is None for b in xyz.box])


def test_are_floats():
    assert _are_floats('6.5', '7.1', '9', '0', '-521.5')
    assert _are_floats(6, 1, -925, 2598.125)
    assert _are_floats('   852.125   ', '   -0.1242   ', '    3    ')
    assert _are_floats('99', '2.1', '-75', '-9285.15', 23, 5.1245, -9, -0.12)

    assert not _are_floats(1, 5.6, '52.1', '8', 'askgj')
    assert not _are_floats(2.1, 3.8, None)
    assert not _are_floats('box:', '125.0', '25.0', '25.0')


def test_read_xyz_velocities():
    file_name_velocities = os.path.join(os.path.dirname(file_name),
                                        'example_velocities_fort.8')
    xyz = Xyz(file_name_velocities)
    xyz.read_file(silent=True)
    assert hasattr(xyz, 'vx')
    assert hasattr(xyz, 'vy')
    assert hasattr(xyz, 'vz')
    assert xyz.vx.shape == xyz.x.shape
    assert xyz.vy.shape == xyz.y.shape
    assert xyz.vz.shape == xyz.z.shape
