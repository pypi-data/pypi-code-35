from distutils.version import StrictVersion as V

from pip import __version__


PIP_VERSION = V(__version__)


def get_dist_from_abstract_dist(abstract_dist, finder):
    if PIP_VERSION >= V("19.0"):
        return abstract_dist.dist()
    else:
        return abstract_dist.dist(finder)
