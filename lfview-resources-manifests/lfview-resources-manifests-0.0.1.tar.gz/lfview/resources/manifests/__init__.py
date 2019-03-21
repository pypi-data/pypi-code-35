"""Manifest resources for LF View API Python client"""
from . import manifests
from .manifests import View, ViewMetadata

__version__ = '0.0.1'

MANIFEST_REGISTRY = manifests._BaseManifest._REGISTRY  #pylint: disable=protected-access
