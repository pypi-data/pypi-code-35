try:
    from distlib.util import cached_property as cached_property_distlib
except ImportError:
    cached_property_distlib = None
