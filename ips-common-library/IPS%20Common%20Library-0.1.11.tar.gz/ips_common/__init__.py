from pbr.version import VersionInfo


_v = VersionInfo('ips_common').semantic_version()
__version__ = _v.release_string()
version_info = _v.version_tuple()

