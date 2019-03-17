__version__ = None

try:
    import pkg_resources
    __version__ = pkg_resources.get_distribution('datasci').version
except Exception:
    pass
