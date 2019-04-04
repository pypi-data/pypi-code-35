import os
import pytest
import numpy as np
from occamtools.generate_fort5 import generate_uniform_random
from occamtools.fort5_to_xyz import fort5_to_xyz, _convert_file_name
from test.test_generate_fort5 import _check_remove_file


def _remove_files(*files):
    for file in files:
        _check_remove_file(file)


def _setup_minimal_fort5(file_name=None, box=None, wrap=False):
    if file_name is None:
        file_name = os.path.join(os.path.dirname(__file__), 'minimal_fort.5')
    n_particles = 10
    if box is None:
        box = [5.153, 6.925, 7.084]
    generate_uniform_random(n_particles, box, file_name)
    return file_name, n_particles, box


def _setup_minimal_and_convert(wrap=False):
    file_name, n_particles, box = _setup_minimal_fort5(wrap=wrap)
    xyz_file_name = fort5_to_xyz(file_name)
    return file_name, n_particles, box, xyz_file_name


def test_fort5_to_xyz_file():
    file_name, _, _ = _setup_minimal_fort5()
    xyz_file_name = fort5_to_xyz(file_name, wrap=False)
    assert xyz_file_name.split('.')[-1] == 'xyz'
    assert _check_remove_file(xyz_file_name)
    _check_remove_file(file_name)


def test_fort5_to_xyz_box():
    file_name, _, _, xyz_file_name = _setup_minimal_and_convert()

    with open(file_name, 'r') as fort5, open(xyz_file_name, 'r') as xyz:
        xyz_line = xyz.readline()
        xyz_line = xyz.readline().split()
        xyz_box = [float(l) for l in xyz_line[2:]]

        fort5_line = fort5.readline()
        fort5_line = fort5.readline().split()
        fort5_box = [float(l) for l in fort5_line[:3]]

        assert np.allclose(xyz_box, fort5_box)

    _remove_files(file_name, xyz_file_name)


def test_fort5_to_xyz_positions():
    file_name, n_particles, _, xyz_file_name = _setup_minimal_and_convert(
        wrap=False
    )

    with open(file_name, 'r') as fort5, open(xyz_file_name, 'r') as xyz:
        for _ in range(2):
            xyz_line = xyz.readline()
        for _ in range(4):
            fort5_line = fort5.readline()

        for _ in range(n_particles):
            for _ in range(3):
                fort5_line = fort5.readline().split()
            fort5_pos = [float(p) for p in fort5_line[4:7]]
            xyz_line = xyz.readline().split()
            xyz_pos = [float(p) for p in xyz_line[1:]]

            for f, x in zip(fort5_pos, xyz_pos):
                assert f == pytest.approx(x, abs=1e-15)

    _remove_files(file_name, xyz_file_name)


def test_fort5_to_xyz_wrap():
    box = [150.0, 50.0, 25.0]
    file_name, n_particles, _ = _setup_minimal_fort5(wrap=True, box=box)
    changed_file = os.path.join(os.path.dirname(file_name), 'changed.5')
    with open(file_name, 'r') as in_file, open(changed_file, 'w') as out_file:
        contents = in_file.readlines()
        new_box = [0.125989589589285, 3.928582514224983, 4.250595259258922]
        contents[1] = '{box_x:.15f} {box_y:.15f} {box_z:.15f}\n'.format(
            box_x=new_box[0], box_y=new_box[1], box_z=new_box[2]
        )
        c = contents[6].split()
        c[4] = '-51.952895859825259'
        c[5] = '-1.0595205025025902'
        c[6] = '-9081.2958928591859825'
        contents[6] = ' '.join(c) + '\n'
        for line in contents:
            out_file.write(line)

    xyz_file_name = fort5_to_xyz(changed_file)

    with open(xyz_file_name, 'r') as in_file:
        for _ in range(2):
            line = in_file.readline()

        for _ in range(n_particles):
            line = in_file.readline().split()
            pos = [float(p) for p in line[1:]]

            for p, box in zip(pos, new_box):
                assert p < box
                assert p > 0.0

    _remove_files(file_name, xyz_file_name, changed_file)


def test_convert_file_name():
    file_name = os.path.join(os.path.dirname(__file__), 'fort.5')
    converted_file = _convert_file_name(file_name)
    converted_file = converted_file.split('.')
    assert converted_file[-1] == 'xyz'

    file_name = os.path.join(os.path.dirname(file_name), 'fort')
    converted_file = _convert_file_name(file_name)
    assert '.' in converted_file
    converted_file = converted_file.split('.')
    assert converted_file[-1] == 'xyz'
