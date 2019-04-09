from tv_extract.extract import extract
from tv_extract._version import get_versions
__version__ = get_versions()['version']
del get_versions

if __name__ == "__main__":
    extract()
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
