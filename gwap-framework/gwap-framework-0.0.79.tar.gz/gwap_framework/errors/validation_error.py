from typing import Dict

from gwap_framework.errors.base import BaseError


class ValidationError(BaseError):
    """
        ValidationException are dispatch when requests is
    """

    def __init__(self, field, message='Invalid field.'):
        BaseError.__init__(self)
        self.code = 400
        self.message = message
        self.status = 'INVALID_FIELD'
        self.field = field

    def to_dict(self) -> Dict:
        result = BaseError.to_dict(self)
        result.setdefault('field', self.field)
        return result

