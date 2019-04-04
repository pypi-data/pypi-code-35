import os
import pytest
import numpy as np
from occamtools.generate_fort5 import generate_uniform_random, generate_fcc


def _check_remove_file(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)
        return True
    else:
        return False


def test_generate_random_uniform_path():
    # Test that path names given result in a file called 'fort.5' created in
    # the given path.
    path = os.path.join(os.path.dirname(__file__), os.pardir)
    path_file = os.path.join(os.path.join(path, 'fort.5'))
    _check_remove_file(path_file)

    generate_uniform_random(1, [1, 1, 1], path=path)
    assert _check_remove_file(path_file)


def test_generate_random_uniform_file():
    # Test that a specific file name given results in a file of that name, at
    # the specified path is created.
    file_name = 'fort.5'
    file_name = os.path.join(os.path.dirname(__file__), file_name)
    _check_remove_file(file_name)

    generate_uniform_random(2, [2, 3, 4], path=file_name)
    assert _check_remove_file(file_name)


def test_generate_random_uniform_header():
    file_name = os.path.join(os.path.dirname(__file__), 'header_test.5')
    _check_remove_file(file_name)

    n_particles = 10
    box = [2, 7, 11]
    generate_uniform_random(n_particles, box, path=file_name)
    assert os.path.exists(file_name)

    with open(file_name, 'r') as in_file:
        # Expected:
        # ---------------------------------------------------------------------
        # Box:
        # 2.00000    7.00000   11.00000    0.00000
        line = in_file.readline().strip()
        assert line.lower() == 'box:'
        line = in_file.readline()
        line = line.split()
        assert len(line) == 4
        for i in range(3):
            assert float(line[i]) == pytest.approx(box[i], abs=1e-15)
            assert float(line[3]) == pytest.approx(0.0, abs=1e-15)

    assert _check_remove_file(file_name)


def test_generate_random_uniform_n_molecules():
    file_name = os.path.join(os.path.dirname(__file__), 'molecules_test.5')
    _check_remove_file(file_name)

    n_particles = 10
    box = [2, 2, 2]
    generate_uniform_random(n_particles, box, path=file_name)
    assert os.path.exists(file_name)

    with open(file_name, 'r') as in_file:
        for _ in range(2):
            line = in_file.readline()

        # Expected:
        # ---------------------------------------------------------------------
        # Number of particles:
        # 10
        line = in_file.readline().strip()
        line = line.split()
        assert len(line) == 3
        expected = ['Number', 'of', 'particles:']
        for i, e in enumerate(expected):
            assert line[i] == e
        line = in_file.readline().strip()
        assert int(line) == n_particles

    assert _check_remove_file(file_name)


def test_generate_random_uniform_positions():
    file_name = os.path.join(os.path.dirname(__file__), 'pos_test.5')
    _check_remove_file(file_name)

    n_particles = 100
    box = [9.29580019,
           6.12879582,
           3.98020502]
    generate_uniform_random(n_particles, box, path=file_name)
    assert os.path.exists(file_name)

    with open(file_name, 'r') as in_file:
        for _ in range(4):
            line = in_file.readline()

        for i in range(1, n_particles+1):
            # Expected:
            # -----------------------------------------------------------------
            # Molecule # 1
            # 1
            # 1 Ar 1 0 0.642649076 3.78051288 3.6288812 0 0 0 0 0 0
            line = in_file.readline()
            line = line.split()
            assert int(line[-1]) == i

            line = in_file.readline().strip()
            assert int(line) == 1

            line = in_file.readline()
            line = line.split()
            assert len(line) == 13
            x, y, z = [float(p) for p in line[4:7]]
            assert x <= box[0]
            assert y <= box[1]
            assert z <= box[2]

    _check_remove_file(file_name)


def test_generate_fcc_box():
    file_name = os.path.join(os.path.dirname(__file__), 'fcc_box_test.5')
    _check_remove_file(file_name)

    lattice_constant = 7.2598259
    cell_box = [3, 1, 4]
    generate_fcc(cell_box, lattice_constant, velocity=False, path=file_name)

    with open(file_name, 'r') as in_file:
        line = in_file.readline()
        line = in_file.readline().split()
        assert len(line) == 4
        expected = [lattice_constant * b for b in cell_box]
        for box, ex in zip(line[:3], expected):
            assert float(box) == pytest.approx(ex, abs=1e-15)

    assert _check_remove_file(file_name)


def test_generate_fcc_box_nonint():
    cell_boxes = np.ones(shape=(5, 3))
    cell_boxes[0, 1] = 10.0
    cell_boxes[1, 2] = 9.0
    cell_boxes[2, 1] = -1
    cell_boxes[3, 0] = 7.1
    cell_boxes[4, 1] = 1.259895
    should_trow = [False,
                   False,
                   True,
                   True,
                   True]
    for should_catch, box in zip(should_trow, cell_boxes):
        caught = False
        try:
            file_name = os.path.join(os.path.dirname(__file__), 'int_test.5')
            _check_remove_file(file_name)
            generate_fcc(box, 1.0, path=file_name)
        except ValueError:
            caught = True
        assert caught is should_catch
        _check_remove_file(file_name)


def test_generate_fcc_n_particles():
    file_name = os.path.join(os.path.dirname(__file__), 'fcc_n_test.5')
    _check_remove_file(file_name)

    lattice_constant = 1.0
    cell_box = [3, 7, 4]
    generate_fcc(cell_box, lattice_constant, velocity=False, path=file_name)

    with open(file_name, 'r') as in_file:
        for _ in range(3):
            line = in_file.readline()

        line = in_file.readline().strip()
        assert float(line) == int(line)
        expected = 4 * np.prod(np.asarray(cell_box))
        assert int(line) == expected

    assert _check_remove_file(file_name)


def test_generate_fcc_positions_velocities():
    file_name = os.path.join(os.path.dirname(__file__), 'fcc_pos_vel_test.5')
    _check_remove_file(file_name)

    lattice_constant = 9.259825981095232
    b = lattice_constant
    cell_box = [3, 2, 4]
    n_particles = generate_fcc(cell_box, b, velocity=True, path=file_name)

    with open(file_name, 'r') as in_file:
        for _ in range(4):
            line = in_file.readline()

        for _ in range(n_particles):
            for _ in range(2):
                line = in_file.readline()
            line = in_file.readline().split()
            assert len(line) == 16
            for p in line[4:7]:
                assert np.mod(float(p), 0.5*b) == pytest.approx(0.0, abs=1e-15)
            for p in line[7:10]:
                assert float(p) == pytest.approx(0.0, abs=1e-15)

    assert _check_remove_file(file_name)
