from enum import Enum


class DataTypeEnum(Enum):
    """
    Defines the known data types for type validation
    """
    INT = 1,
    """integer (e.g. 1)"""
    DECIMAL = 2,
    """numeric value with a decimal point (e.g. 1.2)"""
    DATE = 3
    """
    date (two formats are supported: YYYY MM DD and MM DD YYYY
    with dot, slash, or dash as separators
    """
    BOOL = 4
    """True/False (the data type for all bool options)"""

    @staticmethod
    def fromstr(enum_str):
        if not enum_str:
            return None
        elif enum_str.lower() in ["int", "integer"]:
            return DataTypeEnum.INT
        elif enum_str.lower() in ["decimal", "float"]:
            return DataTypeEnum.DECIMAL
        elif enum_str.lower() in ["date"]:
            return DataTypeEnum.DATE
        elif enum_str.lower() in ["bool"]:
            return DataTypeEnum.BOOL
        else:
            return None

    def tostr(self):
        if self is DataTypeEnum.INT:
            return "int"
        elif self is DataTypeEnum.DECIMAL:
            return "decimal"
        elif self is DataTypeEnum.DATE:
            return "date"
        elif self is DataTypeEnum.BOOL:
            return "bool"
