"""Collection of exceptions datarecords can throw"""


class CannotMutateRecordError(AttributeError):
    """Error message thrown when editing or deleting fields on a data record"""
    pass
