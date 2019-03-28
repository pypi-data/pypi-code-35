from navipy import Brain
from navipy.comparing import weighted_irdf
import pandas as pd
import numpy as np
from navipy.maths.coordinates import spherical_to_cartesian
# 0) Define a class heriting from Brain


def processing(scene, channel):
    """ Return the image difference

    * inverse of distance (i.e. distance -> nearness)
    """
    # Invert distance to nearness
    scene[..., 3, :] = 1 / scene[..., 3, :]
    return scene[..., channel, :]


def comparing(current, memories, viewing_directions):
    """ Calculate homing vector with multi-snaphot irdf

    Used in:
    * Dewar, A. D., Philippides, A., & Graham, P. (2014). \
      What is the relationship between visual environment and \
      the form of ant learning-walks? An in silico investigation \
      of insect navigation.
    """
    if (current.shape[2] != 1) or (memories[0].shape[2] != 1):
        msg = 'Current view {} and the memory {} \n'
        msg += 'should be a NxMx1x1 matrix'
        msg = msg.format(current.shape, memories[0].shape)
        raise NameError(msg)
    # homing_vect_cp is a complex number
    homing_vect_cp = \
        weighted_irdf(current, memories, viewing_directions)
    direction = np.angle(homing_vect_cp, deg=False)
    minval = np.norm(homing_vect_cp)
    homing_vect = spherical_to_cartesian(elevation=0,
                                         azimuth=direction,
                                         radius=minval)
    return homing_vect


class DewarBrain(Brain):
    def __init__(self,
                 memories,
                 renderer=None,
                 channel=0):
        Brain.__init__(self, renderer=renderer)
        # Init memory
        self.channel = channel
        self.memories = memories

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
