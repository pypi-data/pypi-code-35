try:
    from bottle import cached_property as cached_property_bottle
except ImportError:
    cached_property_bottle = None
