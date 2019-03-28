
import numpy as np
import pytest

from rtrace.rtrace import (
    point_in_polygon, ray_x_plane, ray_x_polygon, ray_x_sphere
)

@pytest.mark.parametrize('p', [
    {
        'r0': np.array([ 1.0, 0.0, 0.0 ]), 'rd': np.array([ 1.0, 0.0, 0.0 ]),
        'pn': np.array([-1.0, 0.0, 0.0 ]), 'pp': np.array([ 2.0, 0.0, 0.0 ]),
        'expected': np.array([2.0, 0.0, 0.0])
    },
    {
        'r0': np.array([ 2.0, 3.0, 4.0 ]), 'rd': np.array([ .577, .577, .577 ]),
        'pn': np.array([-1.0, 0.0, 0.0 ]), 'pp': np.array([ 7.0, 0.0, 0.0 ]),
        'expected': np.array([7.0, 8.0, 9.0])
    }
])
def test_ray_x_plane(request, p):
    t = ray_x_plane(p['r0'], p['rd'], p['pp'], p['pn'], tol=1e-6)
    ri = p['r0'] + p['rd'] * t
    assert np.allclose(ri, p['expected'])

@pytest.mark.parametrize('p', [
    {
        'ri': np.array([0.5, 5.0, 0.9]), 'pn': np.array([0.0, 1.0, 0.0]),
        'poly_verts': np.array([
            [ 0.0, 5.0, 0.0 ], [ 0.5, 5.0, 0.5 ],
            [ 1.0, 5.0, 0.0 ], [ 0.5, 5.0, 1.0 ],
        ]),
        'assert': True
    },
    {
        'ri': np.array([0.01, 0.0, 0.02]), 'pn': np.array([0.0, 1.0, 0.0]),
        'poly_verts': np.array([
            [ 0.0, 0.0, 0.0 ], [ 0.5, 0.0, 0.5 ],
            [ 1.0, 0.0, 0.0 ], [ 0.5, 0.0, 1.0 ],
        ]),
        'assert': True
    },
    {
        'ri': np.array([2.0, 0.0, 0.0]), 'pn': np.array([-1.0, 1.0, 0.0]),
        'poly_verts': np.array([
            [ 2.0, -1.0, -1.0 ], [ 2.0, -1.0,  1.0 ],
            [ 2.0,  1.0,  1.0 ], [ 2.0,  1.0, -1.0 ],
        ]),
        'assert': True
    },
])
def test_point_in_poly(request, p):
    assert point_in_polygon(p['ri'], p['poly_verts'], p['pn']) == p['assert']


@pytest.mark.parametrize('p', [
    {
        'r0': np.array([ 1.0, 0.0, 0.0 ]),
        'rd': np.array([ 1.0, 0.0, 0.0 ]),
        'poly_verts': np.array([
            [ 2.0, -1.0, -1.0 ], [ 2.0, -1.0,  1.0 ],
            [ 2.0,  1.0,  1.0 ], [ 2.0,  1.0, -1.0 ],
        ]),
        'pn': np.array([-1.0, 0.0, 0.0 ]),
        'expected': (np.array([2.0, 0.0, 0.0]), True)
    },
])
def test_ray_x_poly(request, p):
    ri, is_inside =  ray_x_polygon(
        p['r0'], p['rd'], p['poly_verts'], p['pn'], tol=1e-6
    )
    assert np.allclose(ri, p['expected'][0])
    assert is_inside == p['expected'][1]


@pytest.mark.parametrize('p', [
    {
        'r0': np.array([ 0.0, 0.0, 0.0 ]),
        'rd': np.array([ 1.0, 2.0, 0.0 ]) / np.linalg.norm([ 1.0, 2.0, 0.0 ]),
        'sc': np.array([ 2.0, 2.0, 0.0 ]),
        'sr': 1.0,
        'expected': (np.array([1.0, 2.0, 0.0]), True)
    },
    {
        'r0': np.array([ 2.0, 0.0, 0.0 ]),
        'rd': np.array([ 0.0, 1.0, 0.0 ]),
        'sc': np.array([ 2.0, 2.0, 0.0 ]),
        'sr': 1.0,
        'expected': (np.array([2.0, 1.0, 0.0]), True)
    },
    {
        'r0': np.array([ 4.0, 0.0, 0.0 ]),
        'rd': np.array([-1.0, 1.0, 0.0 ]) / np.linalg.norm([-1.0, 1.0, 0.0]),
        'sc': np.array([ 2.0, 2.0, 0.0 ]),
        'sr': 1.0,
        'expected': (
            np.array([2.0 + np.cos(np.pi/4.), 2.0 - np.cos(np.pi/4.), 0.0]),
            True
        )
    },
    {
        'r0': np.array([ 4.0, 0.0, 0.0 ]),
        'rd': np.array([ 0.0, 1.0, 0.0 ]),
        'sc': np.array([ 2.0, 2.0, 0.0 ]),
        'sr': 1.0,
        'expected': (np.inf, False)
    },
    {
        'r0': np.array([ 1.0, -2.0, -1.0 ]),
        'rd': np.array([ 1.0,  2.0,  4.0 ]) / np.linalg.norm([ 1.0, 2.0, 4.0 ]),
        'sc': np.array([ 3.0,  0.0,  5.0 ]),
        'sr': 3.0,
        'expected': (np.array([1.81689369, -0.36621263, 2.26757475]), True)
    }
])
def test_ray_x_sphere(request, p):
    ri, hit_sphere = ray_x_sphere(p['r0'], p['rd'], p['sc'], p['sr'])
    assert np.allclose(ri, p['expected'][0])
    assert hit_sphere == p['expected'][1]

