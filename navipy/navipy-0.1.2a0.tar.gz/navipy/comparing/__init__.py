"""
Comparing
"""
import numpy as np
import pandas as pd
from navipy.scene import is_ibpc, is_obpc, check_scene
from navipy.scene import __spherical_indeces__


def simple_imagediff(current, memory):
    """Compute the difference between
the current and memorised place code

    :param current: current place code
    :param memory: memorised place code
    :returns: the image difference
    :rtype: float

    ..ref: Zeil, J., 2012. Visual homing: an insect perspective.
           Current opinion in neurobiology

    """
    if not isinstance(current, np.ndarray):
        raise TypeError('current place code should be a numpy array')
    if not isinstance(memory, np.ndarray):
        raise TypeError('memory place code should be a numpy array')
    if not np.all(current.shape == memory.shape):
        raise Exception('memory and current place code should\
                       have the same shape')
    check_scene(current)
    check_scene(memory)
    diff = current - memory
    if is_ibpc(current):
        return diff
    elif is_obpc(current):
        return diff
    else:
        raise TypeError('place code is neither an ibpc nor obpc')


def imagediff(current, memory):
    """Compute the root mean square difference between
the current and memorised place code

    :param current: current place code
    :param memory: memorised place code
    :returns: the image difference
    :rtype: float #array(1,4) for ibpc and float for obpc

    """
    simple_diff = simple_imagediff(current, memory)
    diff = np.power(simple_diff, 2)
    if is_ibpc(current):
        return np.sqrt(diff.mean(axis=0).mean(axis=0))  # 1
    elif is_obpc(current):
        return np.sqrt(diff.mean(axis=0).mean(axis=0))
    else:
        raise TypeError('place code is neither an ibpc nor obpc')


def rot_imagediff(current, memory):
    """Compute the rotational image difference between
the current and memorised place code.

    :param current: current place code
    :param memory: memorised place code
    :returns: the rotational image difference
    :rtype: (np.ndarray)

    ..ref: Zeil, J., 2012. Visual homing: an insect perspective.
           Current opinion in neurobiology
    ..note: assume that the image is periodic along the x axis
           (the left-right axis)


    """
    if not is_ibpc(current):  # and not is_obpc(current):
        raise TypeError('The current and memory place code\
                       should be image based')
    if not is_ibpc(memory):  # and not is_obpc(memory):
        raise TypeError('The current and memory place code\
                       should be image based')
    check_scene(current)
    check_scene(memory)
    # ridf is a NxM matrix,
    # because one value per azimuth (N) and n values per channel
    # (M)
    ridf = np.zeros((current.shape[1], current.shape[2]))
    for azimuth_i in range(0, current.shape[1]):
        # Perform a counter clock wise rotation
        rot_im = np.roll(current, -azimuth_i, axis=1)
        ridf[azimuth_i, :] = np.squeeze(imagediff(rot_im, memory))  # rot_im
    return ridf


def diff_optic_flow(current, memory):
    """Computes the direction of motion from current
to memory by using the optic flow under the
constrain that the brightness is constant, (small movement),
using a taylor expansion and solving the equation:
.. math::

   0=I_t+\delta I*<u,v> or I_x+I_y+I_t=0

afterwards the aperture problem is solved by a
Matrix equation Ax=b, where x=(u,v) and
.. math::

    A=(I_x,I_y) and b = I_t

The intput parameters are the following:
    :param current: current place code
    :param memory: memorised place code
    :returns: a directional vectors
    :rtype: (np.ndarray)

    ..ref: aperture problem:
           Shimojo, Shinsuke, Gerald H. Silverman, and Ken Nakayama:
           "Occlusion and the solution to the aperture problem for motion."
            Vision research 29.5 (1989): 619-626.
           optic flow:
           Horn, Berthold KP, and Brian G. Schunck.:
           "Determining optical flow."
           Artificial intelligence 17.1-3 (1981): 185-203.
    """
    if not is_ibpc(current):  # and not is_obpc(current):
        raise TypeError('The current and memory place code\
                       should be image based')
    if not is_ibpc(memory):  # and not is_obpc(memory):
        raise TypeError('The current and memory place code\
                       should be image based')
    check_scene(current)
    check_scene(memory)
    currroll = np.roll(current, 1, axis=1)
    dx = current - currroll
    memroll = np.roll(memory, 1, axis=1)
    dy = memory - memroll
    dy = np.reshape(dy, (np.prod(dy.shape), 1))
    dx = np.reshape(dx, (np.prod(dx.shape), 1))
    di = current - memory
    di = np.reshape(di, (np.prod(di.shape), 1))
    a_matrix = np.column_stack([dy, dx])
    a_matrix_sqr = np.dot(np.transpose(a_matrix), a_matrix)
    b_vector = np.dot(np.transpose(a_matrix), di)
    res = np.linalg.solve(a_matrix_sqr, b_vector)
    return res


def gradient(current, memory):
    return 0


def weighted_irdf(current,
                  mem_scenes,
                  viewing_directions):
    """Weighted image rotational difference

    Return an homing vector direction based on an \
    Image rotational difference weighted between \
    some reference snapshots

    :param current: actual scene, np.array
    :param mem_scenes: list of memorised of views
    :returns: dx, dy, dz, dyaw, dpitch, droll.
    :rtypes: pd.Series
    """
    if not isinstance(mem_scenes, (list, tuple)):
        msg = 'mem_scenes should be of type'
        msg += 'list or tuple and not {}'
        msg = msg.format(type(mem_scenes))
        raise TypeError(mem_scenes)
    for scene in mem_scenes:
        check_scene(scene)
    check_scene(current)

    # A dataframe to store
    # the minimum of the irdf and the angle
    # at which the minimum takes place
    df_svp = pd.DataFrame(index=range(0, len(mem_scenes)),
                          columns=['irdf', 'angle'])

    for i, scene in enumerate(mem_scenes):
        irdf = rot_imagediff(current, scene)
        idx = np.argmin(irdf[..., 0])
        value = np.min(irdf[..., 0])
        df_svp.loc[i, 'angle'] = \
            viewing_directions[idx,
                               __spherical_indeces__['azimuth']]
        df_svp.loc[i, 'irdf'] = value

    min_irdf = df_svp.irdf.min()
    # Take the best svp irdf and make the ratio
    # for each others that gives the weighted irdf
    w_svp = min_irdf / df_svp.irdf
    # Weighting of the vector direction based on circular statistics
    j = complex(0, 1)
    H = w_svp * np.exp(df_svp.angle * j)
    return np.sum(H)
