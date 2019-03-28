from navipy import Brain
from navipy.comparing import rot_imagediff
import pandas as pd
import numpy as np
from navipy.scene import __spherical_indeces__
from navipy.maths.coordinates import spherical_to_cartesian
# 0) Define a class heriting from Brain


def processing(scene, channel):
    """ Return the image difference

    * inverse of distance (i.e. distance -> nearness)
    """
    # Invert distance to nearness
    scene[..., 3, :] = 1 / scene[..., 3, :]
    return scene[..., channel, :]


def comparing(current, memory, viewing_directions):
    """ Calculate homing vector with irdf

    irdf: Image rotation difference function
    The image difference is root mean square

    Used in:
    * Zeil, J., Hofmann, M., & Chahl, J. (2003). \
      Catchment Areas of Panoramic Snapshots in Outdoor Scenes.
    * Baddeley, B., Graham, P., Husbands, P., & Philippides, A. (2012).\
      A Model of Ant Route Navigation Driven by Scene Familiarity.
    * Ardin, P., Peng, F., Mangan, M., Lagogiannis, K., & Webb, B. (2016).\
      Using an Insect Mushroom Body Circuit to Encode Route \
      Memory in Complex Natural Environments.
    """
    if (current.shape[2] != 1) or (memory.shape[2] != 1):
        msg = 'Current view {} and the memory {} \n'
        msg += 'should be a NxMx1x1 matrix'
        msg = msg.format(current.shape, memory.shape)
        raise NameError(msg)
    irdf = rot_imagediff(current, memory)
    # [..., 0] because processing
    # select one channel, and therefore
    # irdf should is only a Nx1 matrix
    idx = np.argmin(irdf[..., 0])
    minval = np.min(irdf[..., 0])
    direction = viewing_directions[idx,
                                   __spherical_indeces__['azimuth']]
    homing_vect = spherical_to_cartesian(elevation=0,
                                         azimuth=direction,
                                         radius=minval)
    return homing_vect


class IRDFBrain(Brain):
    def __init__(self,
                 memory,
                 renderer=None,
                 channel=0):
        Brain.__init__(self, renderer=renderer)
        # Init memory
        self.channel = channel
        self.memory = memory

    def velocity(self):
        index = self.posorient.index
        convention = index.levels[0][-1]
        current = processing(self.vision.scene,
                             self.channel)
        homing_vector = comparing(current,
                                  self.memory,
                                  self.vision.viewing_directions,
                                  )
        homing_vector = np.squeeze(homing_vector)
        indeces = [('location', 'dx'), ('location', 'dy'),
                   ('location', 'dz'), (convention, 'dalpha_0'),
                   (convention, 'dalpha_1'), (convention, 'dalpha_2')]
        velocity = pd.Series(data=0, index=pd.MultiIndex.from_tuples(indeces))
        velocity.loc['location'] = homing_vector
        return velocity
