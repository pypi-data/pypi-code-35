from navipy import Brain
from navipy.processing.pcode import apcv, skyline
import pandas as pd
import numpy as np
from navipy.scene import __spherical_indeces__
# 0) Define a class heriting from Brain


def processing(scene, viewing_directions, channel):
    """ Return the average skyline vector by doing

    * inverse of distance (i.e. distance -> nearness)
    * summing along elevation (i.e. estimate of skyline)
    * vector summing of skyline vector

    Average place cell vector on the skyline
    refer as skyline vector:
    * Müller et al. 2018
    * Basten and Mallot 2010
    refer as COMANV in :
    * Hafner 2000,
    * Bertrand 2015
    center of mass of average nearness vector
    """
    # Invert distance to nearness
    scene[..., 3, :] = 1 / scene[..., 3, :]
    # Calculate the skyline
    scene = skyline(scene)
    # skyline viewing direction
    viewdir = viewing_directions[1, ...][np.newaxis, ...]
    viewdir[..., __spherical_indeces__['elevation']] = 0
    comanv = apcv(scene, viewdir)
    return comanv[..., channel, :]


def comparing(current, memory):
    """ Calculate homing vector

    homing vector  = current vector - memory vector
    """
    return current - memory


class ASVBrain(Brain):
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
                             self.vision.viewing_directions,
                             self.channel)
        homing_vector = comparing(current, self.memory)
        homing_vector = np.squeeze(homing_vector)
        indeces = [('location', 'dx'), ('location', 'dy'),
                   ('location', 'dz'), (convention, 'dalpha_0'),
                   (convention, 'dalpha_1'), (convention, 'dalpha_2')]
        velocity = pd.Series(data=0, index=pd.MultiIndex.from_tuples(indeces))
        velocity.loc['location'] = homing_vector
        return velocity
