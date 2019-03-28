"""
 Conversion between coordinates systems
"""
import numpy as np
from navipy.scene import is_numeric_array


def cartesian_to_spherical(x, y, z):
    """ Cartesian to spherical coordinates

    :param x: position along x-axis
    :param y: position along y-axis
    :param z: position along z-axis
    :returns: elevation,azimuth,radius

    inverse transform of :
    x = radius*cos(elevation) * cos(azimuth)
    y = radius*cos(elevation) * sin(azimuth)
    z = radius*sin(elevation)

    """
    radius = np.sqrt(x**2 + y**2 + z**2)
    elevation = np.arctan2(z, np.sqrt(x**2 + y**2))
    azimuth = np.arctan2(y, x)
    spherical = np.zeros_like(x)
    spherical = np.tile(spherical[..., np.newaxis], (3,))
    return elevation, azimuth, radius


def spherical_to_cartesian(elevation, azimuth, radius=1):
    """Spherical to cartesian coordinates

    :param elevation: elevation
    :param azimuth: azimuth
    :param radius: radius
    :returns: x,y,z

    transform :
    x = radius*cos(elevation) * cos(azimuth)
    y = radius*cos(elevation) * sin(azimuth)
    z = radius*sin(elevation)
    """
    x = radius*np.cos(elevation) * np.cos(azimuth)
    y = radius*np.cos(elevation) * np.sin(azimuth)
    z = radius*np.sin(elevation)
    return x, y, z


def cartesian_to_spherical_vectors(cart_vec, viewing_direction):
    """Now we need the cartesian vector as a spherical vecotr.
    A vector in cartesian coordinates can be transform as one in
    the spherical coordinates following the transformation:

    A_rho    =+A_x.*cos(epsilon).*cos(phi)
              +A_y.*cos(epsilon).*sin(phi)
              +A_z.*sin(epsilon)
    A_epsilon=-A_x.*sin(epsilon).*cos(phi)
              -A_y.*sin(epsilon).*sin(phi)
              +A_z.*cos(epsilon)
    A_phi    =-A_x.*sin(phi)+A_y.*cos(phi)

    for epsilon in [-pi/2 +pi/2] and phi in [0 2pi]
    reverse tajectory, needed because the frame x,y,z is expressed in
    the orientation Yaw=pitch=roll=0"""
    if cart_vec is None:
        raise ValueError("cartesian vector must not be None")
    if viewing_direction is None:
        raise ValueError("viewing direction must not be None")
    if (not isinstance(cart_vec, np.ndarray)):
        raise TypeError("vector must be of type np.ndarray")
    if cart_vec.shape[0] != 3:
        raise Exception("first dimension of cartesian vector\
                         must have size three")
    if not is_numeric_array(cart_vec):
        raise TypeError("cartesian vector must be of numerical type")
    if (not isinstance(viewing_direction, list)) and\
       (not isinstance(viewing_direction, np.ndarray)):
        raise TypeError("angles must be list or np.ndarray")
    if not is_numeric_array(viewing_direction):
        raise TypeError("viewing_direction must be of numerical type")
    if len(viewing_direction) != 2:
        raise Exception("first dimension of viewing\
                         direction must be of size two")

    SPH_x = cart_vec[0]
    SPH_y = cart_vec[1]
    SPH_z = cart_vec[2]

    epsilon = viewing_direction[1]
    phi = viewing_direction[0]

    rofterm1 = +SPH_x*np.cos(epsilon)*np.cos(phi)
    rofterm2 = +SPH_y*np.cos(epsilon)*np.sin(phi)
    rofterm3 = +SPH_z*np.sin(epsilon)
    sph_x = rofterm1+rofterm2+rofterm3

    vofterm1 = -SPH_x*np.sin(epsilon)*np.cos(phi)
    vofterm2 = -SPH_y*np.sin(epsilon)*np.sin(phi)
    vofterm3 = SPH_z*np.cos(epsilon)
    sph_z = vofterm1+vofterm2+vofterm3
    sph_y = -SPH_x*np.sin(phi) + SPH_y*np.cos(phi)

    return [sph_x, sph_y, sph_z]
