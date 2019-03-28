"""
Every agent comes with a brain processing the about of \
senses or sensors for biological or technical agent, respectively.

The senses of agents in navipy are limited
to:

* 4d vision (brighness + depth)

The 4d vision sense is controlled by rendering module, either an \
online rendering or loaded from a database containing pre-rendered images.

For example to use pre-rendered images from a database:

.. literalinclude:: example/processing/apcv.py
   :lines: 10-11

Then the brain can be updated at a new position orientation:

.. literalinclude:: example/processing/apcv.py
   :lines: 15

Building your own brain
-----------------------

The Brain class is an abstract Brain, such that it can not control an agent. \
To control, an agent, the Brain should have a function called velocity.

For example, an stationary agent should always return a null velocity.

.. literalinclude:: example/brain/static_brain.py
   :lines: 3,9-17

An agent using an average skyline homing vector, could be build as follow

.. literalinclude:: example/brain/asv_brain.py
   :lines: 4-5,11-36

"""
from navipy.database import DataBase
import logging


class Bunch:
    def __init__(self, **kwds):
        self.__dict__.update(kwds)


class Brain():
    def __init__(self,
                 renderer=None):
        self.vision = Bunch(scene=None,
                            viewing_directions=None,
                            channels=None)
        self.renderer = renderer
        if self.renderer is not None:
            self.vision.scene = None
            self.vision.viewing_directions = renderer.viewing_directions
            self.vision.channels = renderer.channels

    def velocity(self):
        raise NotImplementedError("Subclasses should implement this")

    def update(self, posorient):
        self.posorient = posorient
        if self.renderer is not None:
            self.vision.scene = self.renderer.scene(posorient)

    @property
    def posorients(self):
        if isinstance(self.renderer, DataBase):
            return self.renderer.posorients
        else:
            raise NotImplementedError("Subclasses should implement this, " +
                                      "when renderer is not DataBaseLoad")


def logger(level=logging.INFO, filename='navipy.log'):
    logger = logging.getLogger('navipy')
    logger.setLevel(level)
    # create a file handler
    if filename is not None:
        handler = logging.FileHandler(filename)
        handler.setLevel(level)
        # create a logging format
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        # add the handlers to the logger
        logger.addHandler(handler)


def unittestlogger():
    logger(level=logging.CRITICAL, filename=None)
