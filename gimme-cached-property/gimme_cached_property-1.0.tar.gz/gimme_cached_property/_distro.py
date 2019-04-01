try:
    from distro import cached_property as cached_property_distro
except ImportError:
    cached_property_distro = None
