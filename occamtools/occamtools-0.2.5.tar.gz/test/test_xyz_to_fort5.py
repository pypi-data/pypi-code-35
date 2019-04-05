import os
import pytest
import numpy as np
from test.test_fort5_to_xyz import _remove_files
from test.test_generate_fort5 import _check_remove_file
from occamtools.xyz_to_fort5 import (xyz_to_fort5, _check_box,
                                     _parse_comment_line)


def _generate_minimal_xyz():
    n_particles = 10
    box = [9, 5.5, 3.2]
    file_name = os.path.join(os.path.dirname(__file__), 'minimal.xyz')
    with open(file_name, 'w') as out_file:
        out_file.write(f'{n_particles}\n')
        out_file.write(f'# box: {box[0]:.15f} {box[1]:.15f} {box[2]:.15f}\n')
        x = np.random.uniform(low=0.0, high=box[0], size=(n_particles))
        y = np.random.uniform(low=0.0, high=box[1], size=(n_particles))
        z = np.random.uniform(low=0.0, high=box[2], size=(n_particles))
        label = 'Ar'
        for i in range(n_particles):
            out_file.write(f'{label} {x[i]:.15f} {y[i]:.15f} {z[i]:.15f}\n')
    return file_name, n_particles, box


def test_xyz_to_occam_parse_comment_line():
    lines = ['125.0 25.0 25.0',
             '#125.000000000000000   25.000000000000000   25.000000000000000',
             '# 125.000000000000000   25.000000000000000   25.000000000000000',
             '# 125 25 25',
             '#125 25 25',
             '#box 125 25 25',
             '#box125 25 25',
             '#box:125.000000000000000   25.000000000000000   25.000000000000',
             '#box:125 25 25',
             '#box:125.0 25 25',
             '#box: 125.000000000000000   25.000000000000000   25.00000000000',
             '#box:125 25.0 25',
             '# box:125.000000000000000   25.000000000000000   25.00000000000',
             '# box:125   25   25',
             '# box:125   25.000   25',
             '# box: 125   25   25',
             '# box:  125.000000000000000   25.000000000000000   25.000000000',
             '# box  125.000000000000000   25.000000000000000   25.000000000',
             '# box125.000000000000000   25.000000000000000   25.000000000']
    expected = [125.0, 25.0, 25.0]
    for line in lines:
        box = _parse_comment_line(line)
        assert box == pytest.approx(expected, abs=1e-15)

    line = ''
    box = _parse_comment_line(line)
    assert box is None
    line = '# a b c'
    caught = False
    try:
        box = _parse_comment_line(line)
    except ValueError:
        caught = True
    assert caught


def test_check_box():
    box = [5.29589528, 295.29859815, 21.95820590]
    box_mod = [b for b in box]
    box_mod[0] = box_mod[0] + 1e-3
    caught_none = False
    try:
        _check_box(None, None)
    except ValueError:
        caught_none = True
    assert caught_none

    caught_diff = False
    try:
        _check_box(box, box_mod)
    except ValueError:
        caught_diff = True
    assert caught_diff

    box_ = _check_box(box, box)
    assert np.allclose(box_, box)
    box_ = _check_box(None, box)
    assert np.allclose(box_, box)
    box_ = _check_box(box, None)
    assert np.allclose(box_, box)


def test_xyz_to_fort5_file():
    file_name, _, box = _generate_minimal_xyz()
    tmp_file = os.path.join(os.path.dirname(__file__), 'tmp.5')
    new_file_name = xyz_to_fort5(file_name, False, box, new_file_name=tmp_file)
    assert new_file_name == tmp_file
    assert _check_remove_file(new_file_name)
    os.remove(file_name)


def test_xyz_to_fort5_default_file():
    file_name, _, box = _generate_minimal_xyz()
    new_file_name = xyz_to_fort5(file_name, True, box)
    assert new_file_name == 'fort.5'
    assert _check_remove_file(new_file_name)
    os.remove(file_name)


def test_xyz_to_fort5_header_and_positions():
    xyz_file, _, box = _generate_minimal_xyz()
    fort5_file = xyz_to_fort5(xyz_file, False, box)
    with open(xyz_file, 'r') as xyz, open(fort5_file, 'r') as fort5:
        xyz_n_particles = int(xyz.readline())
        xyz_box = _parse_comment_line(xyz.readline())

        _ = fort5.readline()
        fort5_box = [float(b) for b in fort5.readline().split()[:3]]
        assert np.allclose(xyz_box, fort5_box)

        _ = fort5.readline()
        fort5_n_particles = int(fort5.readline())
        assert fort5_n_particles == xyz_n_particles
        n_particles = xyz_n_particles

        for _ in range(n_particles):
            for _ in range(3):
                fort5_line = fort5.readline()
            fort5_pos = [float(p) for p in fort5_line.split()[4:7]]
            xyz_pos = [float(p) for p in xyz.readline().split()[1:]]
            assert np.allclose(fort5_pos, xyz_pos)
    _remove_files(xyz_file, fort5_file)
