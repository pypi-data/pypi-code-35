try:
    from cached_property import cached_property as cached_property_cached_property
except ImportError:
    cached_property_cached_property = None
