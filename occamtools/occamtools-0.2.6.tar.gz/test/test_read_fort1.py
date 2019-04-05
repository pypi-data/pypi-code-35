import os
import pytest
from occamtools.read_fort1 import _parse_bool, Fort1


def test_parse_bool():
    true = ['YES', 'Y', '1', 'T', 'TRUE']
    false = ['NO', 'N', '0', 'F', 'FALSE']
    for string in true:
        assert _parse_bool(string)
    for string in false:
        assert not _parse_bool(string)

    caught = False
    try:
        _parse_bool('a')
    except ValueError:
        caught = True
    assert caught


def test_read_fort1_file():
    file_name = os.path.join(os.path.dirname(__file__), os.pardir, 'data',
                             'example_fort.1')
    file_name_2 = os.path.join(os.path.dirname(__file__), os.pardir, 'data',
                               'example_2_fort.1')
    fort1 = Fort1(file_name)
    fort1.read_file(silent=True)

    with open(file_name, 'r') as in_file:
        for _ in range(2):
            line = in_file.readline().strip()
        assert line == fort1.title
        assert line == 'example_fort.1'

    fort1.read_file(file_name_2, silent=True)
    with open(file_name_2, 'r') as in_file:
        for _ in range(2):
            line = in_file.readline().strip()
        assert line == fort1.title
        assert line == 'example_2_fort.1'


def test_read_fort1_invalid():
    file_name = os.path.join(os.path.dirname(__file__), 'invalid_fort.1')
    with open(file_name, 'w') as out_file:
        out_file.write('title:\n')
        out_file.write('invalid_fort.1\n')
        out_file.write('invalid_key:\n')
        out_file.write('here be dragons\n')

    caught = False
    try:
        fort1 = Fort1(file_name)
        fort1.read_file(silent=True)
    except ValueError:
        caught = True
    assert caught
    os.remove(file_name)


def test_read_fort1_file_contents():
    file_name = os.path.join(os.path.dirname(__file__), os.pardir, 'data',
                             'example_fort.1')
    fort1 = Fort1(file_name)
    fort1.read_file(silent=True)
    assert fort1.n_particles == 2500
    assert fort1.dt == pytest.approx(0.03, abs=1e-15)
    assert fort1.adaptive_region_start == pytest.approx(50.0, abs=1e-15)

    assert isinstance(fort1.angle_function, int)
    assert isinstance(fort1.temperature_coupl, float)
    assert isinstance(fort1.velocity_read, bool)
