"""
"""
import numpy as np
from navipy.trajectories.triangle import Triangle
from navipy.maths import homogeneous_transformations as ht
from scipy.optimize import minimize

_modes = []
for axel in ['x-axis', 'y-axis', 'z-axis']:
    for marker in range(3):
        _modes.append(axel + '=median-from-{}'.format(marker))

for axel in ['x-axis', 'y-axis', 'z-axis']:
    for marki in range(3):
        for markj in range(3):
            if marki == markj:
                continue
            _modes.append(axel + '={}-{}'.format(marki, markj))


def determine_mode(mode):
    cmode = mode.split('=')
    if len(cmode) != 2:
        raise KeyError('mode should contain one and only one sign =')
    axes = ['x-axis', 'y-axis', 'z-axis']
    if cmode[0] not in axes:
        raise KeyError(
            'left side of sign = should be {}, {}, or {}'.format(
                axes[0], axes[1], axes[2]))
    axel = cmode[0]
    cmode = cmode[1].split('-')
    if len(cmode) == 2:
        apexes = (int(cmode[0]), int(cmode[1]))
        method = 'aligned-with'
    elif len(cmode) == 3:
        apexes = int(cmode[-1])
        method = cmode[0] + '-' + cmode[1]
    return axel, apexes, method


def normalise_vec(vec):
    """Normalise vector when its norm is >0"""
    # assert np.linalg.norm(vec) > 0, 'vec axis has a null norm'
    if np.linalg.norm(vec) > 0:
        vec = vec / np.linalg.norm(vec)
    else:
        vec = vec * np.nan
    return vec


def median_from(triangle, axel, marker):
    """One axel of the body is assumed to be aligned with the median \
       from an apex of the triangle.
    """
    # find next marker
    next_marker = marker + 1
    if next_marker > 2:
        next_marker = 0
    medians = triangle.medians()
    vectors = triangle.apexes2vectors()
    x_axis = medians.loc[:, marker] - triangle.apexes.apex0
    x_axis = x_axis.loc[['x', 'y', 'z']].values
    if ((marker, next_marker) == (0, 1)) or \
       ((marker, next_marker) == (1, 2)) or \
       ((marker, next_marker) == (2, 0)):
        vector = vectors.loc[['x', 'y', 'z'], (marker, next_marker)]
    elif ((next_marker, marker) == (0, 1)) or \
         ((next_marker, marker) == (1, 2)) or \
         ((next_marker, marker) == (2, 0)):
        vector = -vectors.loc[['x', 'y', 'z'], (next_marker, marker)]
    else:
        raise KeyError(
            'Can not compute median from with apexes {}'.format(marker))
    z_axis = np.cross(vector.values,
                      x_axis)
    y_axis = np.cross(z_axis, x_axis)
    x_axis = normalise_vec(x_axis)
    y_axis = normalise_vec(y_axis)
    z_axis = normalise_vec(z_axis)
    if axel == 'x-axis':
        return x_axis, y_axis, z_axis
    elif axel == 'y-axis':
        return y_axis, z_axis, x_axis
    elif axel == 'z-axis':
        return z_axis, x_axis, y_axis
    else:
        raise KeyError('{} axis is not supported'.format(axel))

    return x_axis, y_axis, z_axis


def aligned_with(triangle, axel, markers):
    """One axel of the body is assumed to be aligned with one edge of the triangle.
    """
    # find third marker
    third_marker = None
    for mark in [0, 1, 2]:
        if mark not in markers:
            third_marker = mark
            break

    vectors = triangle.apexes2vectors()
    if (markers == (0, 1)) or \
       (markers == (1, 2)) or \
       (markers == (2, 0)):
        y_axis = vectors.loc[:, (markers[0], markers[1])]
    elif (markers[::-1] == (0, 1)) or \
         (markers[::-1] == (1, 2)) or \
         (markers[::-1] == (2, 0)):
        y_axis = - vectors.loc[['x', 'y', 'z'],
                               (markers[1], markers[0])]
    else:
        raise KeyError(
            'Can not compute aligned-with with apexes {}, {}'.format(
                markers[0], markers[1]))

    y_axis = y_axis.loc[['x', 'y', 'z']].values
    if ((markers[0], third_marker) == (0, 1)) or \
       ((markers[0], third_marker) == (1, 2)) or \
       ((markers[0], third_marker) == (2, 0)):
        vector = - vectors.loc[['x', 'y', 'z'],
                               (markers[0], third_marker)]
    elif ((third_marker, markers[0]) == (0, 1)) or \
        ((third_marker, markers[0]) == (1, 2)) or \
            ((third_marker, markers[0]) == (2, 0)):
        vector = vectors.loc[['x', 'y', 'z'],
                             (third_marker, markers[0])]
    else:
        raise KeyError(
            'Can not compute aligned-with with apexes {}, {}'.format(
                markers[0], markers[1]))

    z_axis = np.cross(vector, y_axis)
    x_axis = np.cross(y_axis, z_axis)

    x_axis = normalise_vec(x_axis)
    y_axis = normalise_vec(y_axis)
    z_axis = normalise_vec(z_axis)

    if axel == 'y-axis':
        return x_axis, y_axis, z_axis
    elif axel == 'x-axis':
        return y_axis, z_axis, x_axis
    elif axel == 'z-axis':
        return z_axis, x_axis, y_axis
    else:
        raise KeyError('{} axis is not supported'.format(axel))


def triangle2bodyaxis(triangle, mode):
    """
    The center of mass of the triangle is the center of all axis of the body.
    The triangle may not be always placed in the same relative to \
the body axis. Therefore several methods can be used to compute \
the body axis from a three points placed on a body. Those methods \
are accesible via the mode.

    modes:
    - 'x-axis=median-from-0'
    - 'y-axis=1-2'
    """
    axel, markers, method = determine_mode(mode)
    origin = triangle.center_of_mass()
    if method == 'median-from':
        x_axis, y_axis, z_axis = median_from(triangle,
                                             axel, markers)
    elif method == 'aligned-with':
        x_axis, y_axis, z_axis = aligned_with(triangle,
                                              axel, markers)
    else:
        print('supported modes')
        print('---------------')
        for m in _modes:
            print(m)
        raise ValueError('mode {} is not supported.'.format(mode))
    return origin, x_axis, y_axis, z_axis


def bodyaxistransformations(x_axis, y_axis, z_axis):
    frame = np.zeros((4, 4))
    frame[:3, 0] = x_axis
    frame[:3, 1] = y_axis
    frame[:3, 2] = z_axis
    frame[3, 3] = 1
    return frame


def triangle2homogeous_transform(triangle, triangle_mode):
    origin, x_axis, y_axis, z_axis = triangle2bodyaxis(triangle, triangle_mode)
    transform = bodyaxistransformations(x_axis, y_axis, z_axis)
    transform[:3, 3] = origin
    return transform


def markers2decompose(mark0, mark1, mark2, triangle_mode,
                      euler_axes, correction=np.eye(4)):
    """ Decompose matrix formed by markers:
    mark0,mark1,mark2

    according to triangle_mode and euler_axes

    homogeneous transformation is corrected by the 4x4coorection matrix as:

    T -> CT
    T: homogeneous_transformations (from markers)
    C: correction matrix (default identity, no correction)
    """
    triangle = Triangle(mark0, mark1, mark2)
    transform = triangle2homogeous_transform(triangle, triangle_mode)
    transform = correction.dot(transform)
    return ht.decompose_matrix(transform, axes=euler_axes)


def markers2euler(mark0, mark1, mark2, triangle_mode,
                  euler_axes, correction=np.eye(4)):
    _, angles = markers2posorient(mark0, mark1, mark2,
                                  triangle_mode, euler_axes, correction)
    return angles


def markers2translate(mark0, mark1, mark2, triangle_mode,
                      euler_axes, correction=np.eye(4)):
    translate, _ = markers2posorient(mark0, mark1, mark2,
                                     triangle_mode, euler_axes, correction)

    return translate


def markers2posorient(mark0, mark1, mark2, triangle_mode,
                      euler_axes, correction=np.eye(4)):
    _, _, angle, translate, _ = markers2decompose(mark0, mark1, mark2,
                                                  triangle_mode, euler_axes,
                                                  correction)
    return translate, angle


def twomarkers2euler_easy_euleraxes(mark0, mark1, axis_alignement,
                                    known_angle):
    """ Determine euler angles from two markers and a known angle

    The functions require a known angle express in the temporary \
rotation convention.

    The known angle is:

    * rotation around x, for axis alignment x-axis
    * rotation around y, for axis alignment y-axis
    * rotation around z, for axis alignment z-axis

    The temporary rotation convention used two determine the euler angles are:

    * zyx, for axis alignment x-axis
    * zxy, for axis alignment y-axis
    * yxz, for axis alignment z-axis

    Note: If you know the angle in your rotation convention, then you \
can run this function through a minimisation procedure with free parameter \
known angle until you get the desired orientation (see twomarkers2euler)

    """
    vector = mark1 - mark0
    vector = normalise_vec(vector)
    if axis_alignement == 'x-axis':
        axes_convention = 'zyx'
        beta = np.arcsin(vector.z)
        alpha = np.arctan2(-vector.y / np.cos(beta),
                           vector.x / np.cos(beta))
        gamma = known_angle
        angles = [alpha, beta, gamma]
    elif axis_alignement == 'y-axis':
        axes_convention = 'zxy'
        gamma = np.arcsin(-vector.z)
        alpha = np.arctan2(vector.x / np.cos(gamma),
                           vector.y / np.cos(gamma))
        beta = known_angle
        angles = [alpha, gamma, beta]
    elif axis_alignement == 'z-axis':
        axes_convention = 'yxz'
        gamma = np.arcsin(vector.y)
        beta = np.arctan2(-vector.x / np.cos(gamma),
                          vector.z / np.cos(gamma))
        alpha = known_angle
        angles = [beta, gamma, alpha]
    else:
        raise KeyError(
            'Axis aligment {} is not supported'.format(
                axis_alignement))
    return angles, axes_convention


def twomarkers2euler_score(x, mark0, mark1,
                           axis_alignement, known_angles, euler_axes):
    """ A root mean square score between wished angles and obtained \
        angles from two markers

    This function is used by twomarkers2euler within the minimisation of scipy
    """
    angles, axes_convention = twomarkers2euler_easy_euleraxes(
        mark0, mark1, axis_alignement, x[0])
    matrix = ht.compose_matrix(
        angles=angles, axes=axes_convention)
    _, _, angles, _, _ = ht.decompose_matrix(matrix, axes=euler_axes)
    return np.nanmean((angles - known_angles)**2)


def twomarkers2euler(mark0, mark1, axis_alignement,
                     known_angle, euler_axes,
                     method='SLSQP', tol=1e-8):
    """ Determine euler angles from two markers and a known angle.

    The known angle is assumed to be the one around the axis aligment.
    If euler_axes contains twice the same axis the first rotation axis is used.

    """
    if axis_alignement not in ['x-axis', 'y-axis', 'z-axis']:
        raise KeyError(
            'Axis aligment {} is not supported'.format(
                axis_alignement))
    known_angles = np.nan * np.zeros(3)
    # Find the first rotation axis
    index = euler_axes.find(axis_alignement[0])
    if index < 0:
        raise KeyError(
            'Axis aligment {} can not work with euler_axes {}'.format(
                axis_alignement, euler_axes))
    if (axis_alignement == 'x-axis') and (euler_axes != 'zyx'):
        msg = 'When x-axis is known, euler_axis zyx should be used\n'
        msg += 'Other convention have not been implemented, sorry'
        raise NameError(msg)
    elif (axis_alignement == 'z-axis') and (euler_axes != 'yxz'):
        msg = 'When z-axis is known, euler_axis yxz should be used\n'
        msg += 'Other convention have not been implemented, sorry'
        raise NameError(msg)
    elif (axis_alignement == 'y-axis') and (euler_axes != 'zxy'):
        msg = 'When y-axis is known, euler_axis zxy should be used\n'
        msg += 'Other convention have not been implemented, sorry'
        raise NameError(msg)

    known_angles[index] = known_angle
    args = (mark0, mark1, axis_alignement, known_angles, euler_axes)
    res = minimize(twomarkers2euler_score, x0=known_angle, args=args,
                   method=method, tol=tol)
    angles, axes_convention = twomarkers2euler_easy_euleraxes(
        mark0, mark1, axis_alignement, res.x[0])
    # Build rotation matrix and decompse
    matrix = ht.compose_matrix(
        angles=angles, axes=axes_convention)
    _, _, angles, _, _ = ht.decompose_matrix(matrix, axes=euler_axes)
    return angles
