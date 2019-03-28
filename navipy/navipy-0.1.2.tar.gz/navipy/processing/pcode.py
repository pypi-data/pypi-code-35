"""
place code derived from scene
"""
import numpy as np
import pandas as pd
from scipy.ndimage import maximum_filter, minimum_filter
from navipy.scene import __spherical_indeces__
from navipy.scene import __cartesian_indeces__
from navipy.scene import __ibpc_indeces__
from navipy.scene import __obpc_indeces__
from navipy.scene import is_ibpc
from navipy.scene import is_obpc
from navipy.maths.coordinates import spherical_to_cartesian
from navipy.scene import check_scene
from navipy.scene import check_viewing_direction


def skyline(scene):
    """Return the average along the elevation of a scene

    :param scene: the scenery at a given location (a 4d numpy array)
    :returns: the skyline [1,azimuth,channel,1]
    :rtype: np.ndarray

    """
    if not is_ibpc(scene):
        raise TypeError('scene should be image based to compute a skyline')
    check_scene(scene)
    skyline = scene.mean(axis=__ibpc_indeces__['elevation'])
    return skyline[np.newaxis, :]


def michelson_contrast(scene, size=3):
    """Return the michelson constrast

    .. math::

       \\frac{I_\\text{max}-I_\\text{min}}{I_\\text{max}+I_\\text{min}}

    with :math:`I_\\text{max}` and :math:`I_\\text{min}` representing the \
highest and lowest luminance in an image region around each pixel.

    :param scene: an image based scene
    :param size: the size of the region to calculate the maximum \
and minimum of the local image intensity
    :returns: the michelson-contrast
    :rtype: np.ndarray

    """
    check_scene(scene)
    if not is_ibpc(scene):
        raise TypeError('scene should be image based\
                       to compute the michelson constrast')
    if not isinstance(size, int):
        raise TypeError('size must be integer')
    if (size < 2 or size > 5):
        raise ValueError('size must be between 2 and 5')
    contrast = np.zeros_like(scene)
    for channel in range(scene.shape[__ibpc_indeces__['channel']]):
        i_max = maximum_filter(scene[..., channel, 0],
                               size=size, mode='wrap')
        i_min = minimum_filter(scene[..., channel, 0],
                               size=size, mode='wrap')
        divider = i_max + i_min
        nonzero = divider != 0
        eqzero = divider == 0
        i_min = i_min[nonzero]
        i_max = i_max[nonzero]
        divider = divider[nonzero]
        contrast[nonzero, channel, 0] = (i_max - i_min) / divider
        contrast[eqzero, channel, 0] = 0
    return contrast


def contrast_weighted_nearness(scene, contrast_size=3, distance_channel=3):
    """Return the michelson contrast wheighted nearness

    :param scene: an image based scene
    :param contrast_size: the size of the region to calculate the maximum \
and minimum of the local image intensity in the michelson-contrast.
    :param distance_channel: the index of the distance-channel.

    """
    check_scene(scene)
    if not isinstance(contrast_size, int):
        raise TypeError('constrast size must be of type integer')
    if not isinstance(distance_channel, int):
        raise TypeError('distance channel must be of type integer')
    if contrast_size not in range(2, 6):
        raise ValueError('contrast size out of range')
    if distance_channel not in range(4):
        raise ValueError('distance channel out of range')
    if not is_ibpc(scene):
        raise TypeError('scene should be image based to\
                       compute the contrast weighted nearness')
    contrast = michelson_contrast(scene, size=contrast_size)
    distance = scene[..., distance_channel, 0]
    distance = distance[..., np.newaxis, np.newaxis]
    distance = np.tile(distance, (1, 1, scene.shape[-2], 1))
    return contrast / distance


def pcv(place_code, viewing_directions):
    """Place code vectors

    :param place_code: the place code at a given location (e.g. an ibs scene)
    :param viewing_directions: viewing direction of each pixel
    :returns: the place code vectors in cartesian coordinates
    :rtype: (np.ndarray)

    """
    # print("place code shape",place_code.shape)
    if is_ibpc(place_code):
        component_dim = __ibpc_indeces__['component']
        channel_dim = __ibpc_indeces__['channel']
    elif is_obpc(place_code):
        component_dim = __obpc_indeces__['component']
        channel_dim = __obpc_indeces__['channel']
    else:
        raise TypeError('place code should be either an ibpc or obpc')

    check_scene(place_code)
    check_viewing_direction(viewing_directions)
    if not place_code.shape[0] == viewing_directions.shape[0]:
        raise Exception('dimensions of place code and viewing\
                       direction do not match')
    if not place_code.shape[1] == viewing_directions.shape[1]:
        raise Exception('dimensions of place code and viewing\
                       direction do not match')
    if not isinstance(viewing_directions, np.ndarray):
        raise TypeError('viewing_directions should be a numpy array')
    if not place_code.shape[component_dim] == 1:
        raise Exception('the last dimension ({}) of the place-code\
                       should be 1'.format(place_code.shape[component_dim]))
    elevation = viewing_directions[..., __spherical_indeces__['elevation']]
    azimuth = viewing_directions[..., __spherical_indeces__['azimuth']]
    if (np.any(elevation <= -np.pi) or np.any(elevation >= np.pi)):
        raise ValueError(" Elevation must be radians in range [-pi;pi]")
    if (np.max(elevation) - np.min(elevation) >= 2 * np.pi):
        raise ValueError(" max difference in elevation must be < 2*pi")
    if (np.any(azimuth <= -2*np.pi) or np.any(azimuth >= 2*np.pi)):
        raise ValueError(" Azimuth must be radians in range [-2*pi;2*pi]")
    if (np.max(azimuth) - np.min(azimuth) > 2 * np.pi):
        raise ValueError(" max difference in azimuth must be <= 2*pi")
    x, y, z = spherical_to_cartesian(elevation, azimuth, radius=1)
    unscaled_lv = np.zeros((viewing_directions.shape[0],
                            viewing_directions.shape[1],
                            3))
    unscaled_lv[..., __cartesian_indeces__['x']] = x
    unscaled_lv[..., __cartesian_indeces__['y']] = y
    unscaled_lv[..., __cartesian_indeces__['z']] = z
    scaled_lv = np.zeros_like(place_code)
    # (3,) -> (1,1,3) or (1,1,1,3) see numpy.tile
    scaled_lv = np.tile(scaled_lv, (unscaled_lv.shape[-1],))
    for channel_index in range(0, scaled_lv.shape[channel_dim]):
        radius = np.tile(place_code[..., channel_index, 0]
                         [..., np.newaxis], (scaled_lv.shape[-1],))
        scaled_lv[..., channel_index, :] = unscaled_lv * radius
    return scaled_lv


def apcv(place_code, viewing_directions):
    """Calculate the average scene vector

    :param place_code: the place code at a given location (e.g. an ibs scene)
    :param viewing_directions: viewing direction of each pixel
    :returns: the average place-code vector
    :rtype: (np.ndarray)

    """
    check_scene(place_code)
    check_viewing_direction(viewing_directions)
    if not place_code.shape[0] == viewing_directions.shape[0]:
        raise Exception('dimensions of place code and viewing\
                      direction do not match')
    if not place_code.shape[1] == viewing_directions.shape[1]:
        raise Exception('dimensions of place code and viewing\
                       direction do not match')
    scaled_lv = pcv(place_code, viewing_directions)
    if is_ibpc(place_code):
        return (scaled_lv.sum(axis=0).sum(axis=0))[np.newaxis, np.newaxis, ...]
    elif is_obpc(place_code):
        return (scaled_lv.sum(axis=0))[np.newaxis, ...]
    else:
        raise TypeError('place code is neither an ibpc nor obpc')


def nposorient_around_ref(mydb,
                          position_df,
                          ref_pos,
                          nb_snapshot,
                          radius,
                          blender_view):
    """Return  set of views around and oriented towards memorized location
    :param mydb: Database environment
    :param position_df: dataframe with the positions of the grid
    :param ref_pos: df with x, y and z position of the reference snapshot
    :param nb_snapshot: number of wanted set of views (multiple of 2)
    :param radius: distance from memorized location to take snapshots
    :param blender_view: viewing axis camera id y=90, if x=0
    :returns: list  of reoriented image array, snaphots positions
    :rtypes:  array of np.array, pd.DataFrame
    """

    svp_all = pd.DataFrame(columns=['x', 'y', 'z', 'frame'])
    # angle of rotation
    ang_deg = 360 / nb_snapshot
    ang = np.deg2rad(ang_deg)
    # make the different view
    for i in range(0, nb_snapshot):
        x = ref_pos.x + radius * np.cos(ang * i)
        y = ref_pos.y + radius * np.sin(ang * i)
        z = ref_pos.z
        svp_frame = pd.Series(index=['frame', 'x', 'y', 'z'])
        distance_arr = pd.Series(index=position_df.index)
        for index, pos in position_df.dropna().iterrows():
            distance = (pos.x - x)**2
            distance += (pos.y - y)**2
            distance += (pos.z - z)**2
            distance_arr[index] = distance
        svp_frame.frame = int(distance_arr.dropna().argmin())
        svp_frame.x = position_df.x[svp_frame.frame]
        svp_frame.y = position_df.y[svp_frame.frame]
        svp_frame.z = position_df.z[svp_frame.frame]
        svp_all.loc[i] = [svp_frame.x, svp_frame.y,
                          svp_frame.z, int(svp_frame.frame)]
    reoriented_mem = []
    rot = list()

    for i, j in svp_all.iterrows():
        ide = int(j.frame)
        image = mydb.scene(rowid=ide)
        alpha = np.floor(np.rad2deg(np.arctan2(
            (ref_pos.y - j.y), (ref_pos.x - j.x))))
        alpha = alpha + blender_view  # because y view on blender
        rot.append(alpha)
        alpha = int(alpha)
        svp_reorient = np.roll(image, alpha, 1)
        reoriented_mem.append(svp_reorient)
    return reoriented_mem, svp_all
