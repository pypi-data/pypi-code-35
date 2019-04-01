try:
    from pip._internal.utils.misc import cached_property as cached_property_pip_internal
except ImportError:
    cached_property_pip_internal = None

try:
    from pip._vendor.distlib.util import cached_property as cached_property_pip_vendor_distlib
except ImportError:
    cached_property_pip_vendor_distlib = None

try:
    from pip._vendor.distro import cached_property as cached_property_pip_vendor_distro
except ImportError:
    cached_property_pip_vendor_distro = None
