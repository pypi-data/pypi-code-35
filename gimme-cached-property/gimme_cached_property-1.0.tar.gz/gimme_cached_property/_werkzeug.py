try:
    from werkzeug.utils import cached_property as cached_property_werkzeug
except ImportError:
    cached_property_werkzeug = None
