"""
 Define what a scene is
"""
import numpy as np


#
# Define constants
#
__spherical_indeces__ = {'elevation': 0,
                         'azimuth': 1,
                         'radius': 2}
__cartesian_indeces__ = {'x': 0,
                         'y': 1,
                         'z': 2}
__ibpc_indeces__ = {'elevation': 0,
                    'azimuth': 1,
                    'channel': 2,
                    'component': 3}
__obpc_indeces__ = {'ommatidia': 0,
                    'channel': 1,
                    'component': 2}
__eye_indeces__ = {'elevation': 0,
                   'azimuth': 1,
                   'component': 2}
__ommadia_indeces__ = {'ommatidia': 0,
                       'component': 1}


def spherical_indeces():
    return {'elevation': 0,
            'azimuth': 1,
            'radius': 2}


def cartesian_indeces():
    return {'x': 0,
            'y': 1,
            'z': 2}


def check_scene(scene):
    if is_ibpc(scene):
        #  print("normal")
        if not is_numeric_array(scene):
            raise TypeError('scene is of non numeric type')
        if not ~np.any(np.isnan(scene)):
            raise ValueError('scene contains nans')
        if not len(scene.shape) == 4:
            raise Exception('scene has wrong shape, must have 4 dimensions')
        if not (scene.shape[1] > 0):
            raise Exception('scenes first dimension is empty')
        if not (scene.shape[0] > 0):
            raise Exception('scenes second dimension is empty')
        if not (scene.shape[2] == 4):
            raise Exception('3rd dimension of scene must be four')
        if not (scene.shape[3] == 1):
            raise Exception('4rd dimension of scene must be one')
        # assert ~(np.any(np.isNone(scene)))
        return True

    elif is_obpc(scene):
        if not is_numeric_array(scene):
            raise TypeError('scene is of non numeric type')
        if not ~np.any(np.isnan(scene)):
            raise ValueError('scene contains nans')
        if not len(scene.shape) == 3:
            raise Exception('scene has wrong shape, must have 4 dimensions')
        if not ~(scene.shape[1] <= 0):
            raise Exception('scenes first dimension is empty')
        if not ~(scene.shape[0] <= 0):
            raise Exception('scenes second dimension is empty')
        if not (scene.shape[2] == 4):
            raise Exception('3rd dimension of scene must be four')
        # assert ~(np.any(np.isNone(scene)))
        return True


def check_viewing_direction(viewing_direction):
    if not is_numeric_array(viewing_direction):
        raise TypeError('viewing direction is of non numeric type')
    if not ~np.any(np.isnan(viewing_direction)):
        raise ValueError('viewing direction contains nans')
    if len(viewing_direction.shape) < 3:
        raise Exception('viewing direction must have at least 3 dimensions')
    if not (viewing_direction.shape[1] > 0):
        raise Exception('viewing direction has empty second dimension')
    if not (viewing_direction.shape[0] > 0):
        raise Exception('viewing direction has empty first dimension')
    if not (viewing_direction.shape[-1] == 2):
        raise Exception(' last dimension of viewing direction must equal 2')
    return True


def is_numeric_array(array):
    """Checks if the dtype of the array is numeric.

    Booleans, unsigned integer, signed integer, floats and complex are
    considered numeric.

    :param array : `numpy.ndarray`-like The array to check.
    :returns: True if it is a recognized numerical and False \
    if object or  string.
    :rtype:bool
    """
    numerical_dtype_kinds = {'b',  # boolean
                             'u',  # unsigned integer
                             'i',  # signed integer
                             'f',  # floats
                             'c'}  # complex
    try:
        return array.dtype.kind in numerical_dtype_kinds
    except AttributeError:
        # in case it's not a numpy array it will probably have no dtype.
        return np.asarray(array).dtype.kind in numerical_dtype_kinds


def is_ibpc(place_code):
    """Test if a place code is image based

    :param place_code: a place-code
    :returns: True if image based place-code
    :rtype: bool

    """
    toreturn = isinstance(place_code, np.ndarray)
    toreturn = toreturn and (len(place_code.shape) ==
                             len(__ibpc_indeces__))
    return toreturn


def is_obpc(place_code):
    """Test if a place code is ommatidia based

    :param place_code: a place-code
    :returns: True if ommatidia based place-code
    :rtype: bool

    """
    toreturn = isinstance(place_code, np.ndarray)
    toreturn = toreturn and (len(place_code.shape) ==
                             len(__obpc_indeces__))
    return toreturn


def ibs_to_obs(scene, eye_map):
    """Convert an image based scene to an ommatidium based scene.

    :param scene: The scene to be converted
    :param eye_map: The eye_map to use
    :returns: (obs_scene,ommatidia_map)
    :rtype: (np.ndarray,np.ndarray)
    """
    assert is_ibpc(scene),\
        'scene should be an ibs scene'
    assert isinstance(eye_map, np.ndarray), 'eye_map should be a numpy array'
    assert len(eye_map.shape) == len(__eye_indeces__),\
        'eye_map should have {} dimensions to be an ibs scene'.format(
            len(__eye_indeces__))
    for index_name in ['elevation', 'azimuth']:
        index = __ibpc_indeces__[index_name]
        assert eye_map.shape[index] == scene.shape[index],\
            'eye_map and scene should have the same number of {}'.format(
                index_name)
    obs_size = (scene.shape[__ibpc_indeces__['elevation']] *
                scene.shape[__ibpc_indeces__['azimuth']],
                scene.shape[__ibpc_indeces__['channel']],
                scene.shape[__ibpc_indeces__['component']])
    obs_scene = scene.reshape(obs_size)
    omm_size = (eye_map.shape[__ibpc_indeces__['elevation']] *
                eye_map.shape[__ibpc_indeces__['azimuth']],
                eye_map.shape[__ibpc_indeces__['component']])
    ommatidia_map = eye_map.reshape(omm_size)
    return (obs_scene, ommatidia_map)
