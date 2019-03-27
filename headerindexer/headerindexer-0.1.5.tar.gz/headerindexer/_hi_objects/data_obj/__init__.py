"""Accessible aggregate of Data documents and factory object 'build'"""


class _DataFactory:
    """Factory to build dataclass objects. Import build below for use"""

    @staticmethod
    def new_work_obj():
        """Call to build, init, and return a new Work object"""
        from ._workings import Work
        return Work()

    @staticmethod
    def new_errors_obj():
        """Call to build, init, and return a new errors object"""
        from ._errors import Errors
        return Errors()


DF_BUILD = _DataFactory()
"""Importable factory to build dataclass objects"""
